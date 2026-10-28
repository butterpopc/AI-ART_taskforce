#!/usr/bin/env python3
"""Exact, sequential Danbooru artist aggregation. Python 3.10+; pyarrow, requests.

Only metadata is downloaded. Checkpoints are local pickle files: never resume
from a checkpoint supplied by somebody else. See ARTIST_METRICS.md.
"""
import argparse
from collections import Counter
import csv
from datetime import datetime, timezone
import hashlib
import io
import json
import math
from pathlib import Path
import pickle
import sys
import time

import pyarrow.parquet as pq
import requests

DATASET = "trojblue/danbooru2025-metadata"
DATA_REV = "41aa4590032d1f742b051e5bbfe6094dc21aa854"
TAG_REV = "209b1dd76b69e95ba6b1619ea5d13e68446607b7"
TAG_URL = "https://raw.githubusercontent.com/DominikDoom/a1111-sd-webui-tagcomplete/{}/tags/danbooru.csv"
EXCLUDED = "bb_(baalbuddy)"
LOW = frozenset("comic 4koma sketch monochrome greyscale meme lineart".split())
CONTENT_TAGS = frozenset("shiny_skin mature_female".split())
CONTENT_COL = "내용태그비율(mature_female·shiny_skin)"
COLS = ["tag_string_artist", "score", "fav_count", "tag_string_general",
        "rating", "created_at", "is_deleted"]
HEADERS = ["순위", "태그", "게시물수_태그목록", "posts", "score_mean",
           "score_median", "score_norm", "fav_mean", "low_ratio", CONTENT_COL,
           "g", "s", "q", "e", "last_post", "플래그", "pool1_포함", "평균_순위", "상위40_등장"]
VERSION = 2


def get(url):
    r = requests.get(url, timeout=(30, 120))
    r.raise_for_status()
    return r


def candidates(raw):
    rows = [r for r in csv.reader(io.StringIO(raw.decode("utf-8-sig")))
            if len(r) >= 3 and r[1] == "1"]
    assert len(rows) == 59201, f"Artist count changed: {len(rows)}"
    # Stable sort: preserve original CSV order for equal post counts.
    rows = sorted((r for r in rows if r[0] != EXCLUDED), key=lambda r: -int(r[2]))[:5000]
    assert len({r[0] for r in rows}) == 5000
    assert (rows[0][0], int(rows[0][2])) == ("ebifurya", 5924)
    assert (rows[-1][0], int(rows[-1][2])) == ("jiekuijiangshadaonijiamenkou", 271)
    assert next(i + 1 for i, r in enumerate(rows) if r[0] == "quasarcake") == 4518
    return [(r[0], int(r[2])) for r in rows]


def new_artist():
    return {"n": 0, "scores": Counter(), "year_sum": Counter(),
            "year_n": Counter(), "fav": 0, "low": 0, "content": 0,
            "rating": Counter(), "last": None}


def new_state(tags, tag_sha, files):
    return {"version": VERSION, "dataset_revision": DATA_REV,
            "tag_revision": TAG_REV, "tag_sha256": tag_sha, "candidates": tags,
            "files": files, "completed": [], "artists": {t: new_artist() for t in
            [t for t, _ in tags] + [EXCLUDED]}, "years": {}, "rows": 0,
            "deleted": 0, "kept": 0, "multi_artist": 0,
            "first": None, "last": None, "started_at": datetime.now(timezone.utc).isoformat()}


def consume(s, data):
    for artists, score, fav, general, rating, created, deleted in zip(*(data[c] for c in COLS)):
        s["rows"] += 1
        if deleted is True:
            s["deleted"] += 1
            continue
        if deleted is not False:
            raise ValueError("Missing/invalid is_deleted; cannot silently include")
        if not isinstance(score, int) or isinstance(score, bool):
            raise ValueError("Missing/noninteger score")
        if not isinstance(fav, int) or isinstance(fav, bool):
            raise ValueError("Missing/noninteger fav_count")
        if not isinstance(artists, str) or not isinstance(general, str):
            raise ValueError("Missing tag string")
        if rating not in ("g", "s", "q", "e"):
            raise ValueError(f"Unexpected rating: {rating!r}")
        dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            raise ValueError("Timezone missing")
        year = dt.year  # Calendar year as recorded in source, not UTC-converted year.
        dt = dt.astimezone(timezone.utc)
        s["kept"] += 1
        s["first"] = min(s["first"], dt) if s["first"] else dt
        s["last"] = max(s["last"], dt) if s["last"] else dt
        s["years"].setdefault(year, Counter())[score] += 1
        atags = set(artists.split())
        s["multi_artist"] += len(atags) > 1
        matches = atags.intersection(s["artists"])
        if not matches:
            continue
        gtags = set(general.split())
        low, content = bool(LOW & gtags), bool(CONTENT_TAGS & gtags)
        for tag in matches:
            a = s["artists"][tag]
            a["n"] += 1
            a["scores"][score] += 1
            a["year_sum"][year] += score
            a["year_n"][year] += 1
            a["fav"] += fav
            a["low"] += low
            a["content"] += content
            a["rating"][rating] += 1
            a["last"] = max(a["last"], dt) if a["last"] else dt


def hist_median(hist):
    n = sum(hist.values())
    if not n:
        return None
    left, right, count, a = (n - 1) // 2, n // 2, 0, None
    for value, freq in sorted(hist.items()):
        count += freq
        if a is None and count > left:
            a = value
        if count > right:
            return (a + value) / 2
    raise AssertionError("Invalid histogram")


def quantile(values, q):
    values = sorted(v for v in values if v is not None)
    if not values:
        return None
    idx = (len(values) - 1) * q
    lo, hi = math.floor(idx), math.ceil(idx)
    return values[lo] + (values[hi] - values[lo]) * (idx - lo)


def metrics(a, medians):
    n = a["n"]
    row = {k: None for k in HEADERS[4:15]}
    row["posts"] = n
    if not n:
        return row
    row.update(score_mean=sum(k * v for k, v in a["scores"].items()) / n,
               score_median=hist_median(a["scores"]), fav_mean=a["fav"] / n,
               low_ratio=a["low"] / n,
               last_post=a["last"].isoformat())
    row[CONTENT_COL] = a["content"] / n
    # Sum(score / year_median) == sum(year_score_sum / year_median).
    # Do not drop affected posts or invent an epsilon when a divisor is zero.
    if all(medians.get(y) not in (None, 0) for y in a["year_n"]):
        row["score_norm"] = math.fsum(a["year_sum"][y] / medians[y]
                                      for y in sorted(a["year_n"])) / n
    row.update({r: a["rating"][r] / n for r in ("g", "s", "q", "e")})
    return row


def download(item, work):
    path = work / Path(item["path"]).name
    url = f"https://huggingface.co/datasets/{DATASET}/resolve/{DATA_REV}/{item['path']}"
    for attempt in range(3):
        try:
            digest = hashlib.sha256()
            with requests.get(url, stream=True, timeout=(30, 120)) as r:
                r.raise_for_status()
                with path.open("wb") as out:
                    for chunk in r.iter_content(4 * 1024 * 1024):
                        out.write(chunk)
                        digest.update(chunk)
            if path.stat().st_size != item["size"]:
                raise ValueError("Download size mismatch")
            expected = item.get("lfs", {}).get("oid")
            if expected and digest.hexdigest() != expected:
                raise ValueError("Download SHA256 mismatch")
            return path, digest.hexdigest()
        except (requests.RequestException, ValueError):
            path.unlink(missing_ok=True)
            if attempt == 2:
                raise
            time.sleep(2 ** attempt)


def save_checkpoint(state, path):
    tmp = path.with_suffix(".tmp")
    with tmp.open("wb") as out:
        pickle.dump(state, out, protocol=pickle.HIGHEST_PROTOCOL)
    tmp.replace(path)


def fmt(value):
    if value is None:
        return "미확인"
    if isinstance(value, float):
        return f"{value:.8g}"
    return str(value)


def table(rows, cols):
    def cell(value):
        return fmt(value).replace("|", "\\|")
    return "\n".join(["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"] +
                     ["| " + " | ".join(cell(r.get(c)) for c in cols) + " |" for r in rows])


def normalize_tag(value):
    """Only space/underscore normalization used by the provided pool; no aliases."""
    return "_".join(value.strip().split())


def load_user_inputs(pool_path, ranks_path):
    pool_raw, ranks_raw = pool_path.read_bytes(), ranks_path.read_bytes()
    names = [normalize_tag(t) for t in pool_raw.decode("utf-8-sig").split(",") if t.strip()]
    if len(names) != len(set(names)):
        raise ValueError("Duplicate normalized pool tags")
    ranks = {}
    for row in csv.DictReader(io.StringIO(ranks_raw.decode("utf-8-sig"))):
        tag = normalize_tag(row["태그"])
        if not tag or tag in ranks:
            raise ValueError("Missing/duplicate rank tag")
        average, top = float(row["평균_순위"]), int(row["상위40_등장"])
        appearances = int(row["등장_조합수"])
        if not math.isfinite(average) or not 1 <= average <= 200 or not 0 <= top <= appearances or appearances < 1:
            raise ValueError("Invalid user rank record")
        ranks[tag] = {"평균_순위": average, "상위40_등장": top}
    sources = {"pool1": {"file": pool_path.name, "sha256": hashlib.sha256(pool_raw).hexdigest(), "tags": len(names)},
               "ranks": {"file": ranks_path.name, "sha256": hashlib.sha256(ranks_raw).hexdigest(), "tags": len(ranks)}}
    return set(names), ranks, sources


def average_ranks(values):
    order = sorted(range(len(values)), key=values.__getitem__)
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i + 1
        while j < len(order) and values[order[j]] == values[order[i]]:
            j += 1
        for k in range(i, j):
            ranks[order[k]] = (i + 1 + j) / 2
        i = j
    return ranks


def spearman(pairs):
    pairs = [(float(x), float(y)) for x, y in pairs
             if x not in (None, "") and y not in (None, "")
             and math.isfinite(float(x)) and math.isfinite(float(y))]
    n = len(pairs)
    if n < 2:
        return None, n
    x, y = (average_ranks(list(v)) for v in zip(*pairs))
    mean = (n + 1) / 2
    x, y = [v - mean for v in x], [v - mean for v in y]
    denom = math.sqrt(math.fsum(v*v for v in x) * math.fsum(v*v for v in y))
    return (math.fsum(a*b for a, b in zip(x, y)) / denom if denom else None), n


def correlation_description(rho):
    if rho is None:
        return "산출 불가(표본 부족 또는 상수값)"
    magnitude = abs(rho)
    strength = "거의 없음" if magnitude < .1 else "약함" if magnitude < .3 else "중간" if magnitude < .5 else "큼"
    direction = "값이 클수록 평균 순위가 나쁜 방향" if rho > 0 else "값이 클수록 평균 순위가 좋은 방향" if rho < 0 else "방향 없음"
    return f"{strength}; {direction}"


def flags_for(row):
    flags = []
    if row["low_ratio"] is not None and row["low_ratio"] >= .5:
        flags.append("흑백만화비중높음")
    if row["posts"] < 30:
        flags.append("표본부족")
    return ";".join(flags)


def finish(s, output, pool, ranks, user_sources):
    assert len(s["completed"]) == 43, "Refuse to publish partial results"
    assert s["rows"] == s["kept"] + s["deleted"]
    assert sum(sum(h.values()) for h in s["years"].values()) == s["kept"]
    medians = {y: hist_median(h) for y, h in s["years"].items()}
    rows = []
    for i, (tag, source_count) in enumerate(s["candidates"], 1):
        a = s["artists"][tag]
        assert sum(a["scores"].values()) == sum(a["year_n"].values()) == sum(a["rating"].values()) == a["n"]
        assert sum(k*v for k, v in a["scores"].items()) == sum(a["year_sum"].values())
        assert 0 <= a["low"] <= a["n"] and 0 <= a["content"] <= a["n"]
        row = {"순위": i, "태그": tag, "게시물수_태그목록": source_count, **metrics(a, medians),
               "pool1_포함": int(tag in pool), "평균_순위": "", "상위40_등장": ""}
        row.update(ranks.get(tag, {}))
        row["플래그"] = flags_for(row)
        rows.append(row)
    comparisons = []
    for c in ["score_norm", "fav_mean", "low_ratio", CONTENT_COL, "g", "s", "q", "e"]:
        rho, n = spearman([(r[c], r["평균_순위"]) for r in rows])
        comparisons.append({"지표": c, "Spearman_rho": rho, "n": n, "해석": correlation_description(rho)})
    output.mkdir(parents=True, exist_ok=True)
    with (output / "artist_metrics_top5000.csv").open("w", encoding="utf-8-sig", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows({k: "미확인" if v is None else v for k, v in r.items()} for r in rows)
    high_low = sorted((r for r in rows if "흑백만화비중높음" in r["플래그"]), key=lambda r: (-r["posts"], r["순위"]))
    columns = ["게시물수_태그목록", "posts", "score_mean", "score_median", "score_norm", "fav_mean",
               "low_ratio", CONTENT_COL, "g", "s", "q", "e", "평균_순위", "상위40_등장"]
    distribution = [{"지표": c, "유효 작가 수": sum(r[c] not in (None, "") for r in rows),
                     **{label: quantile([r[c] for r in rows if r[c] != ""], q) for label, q in
                        [("최소", 0), ("Q1", .25), ("중앙값", .5), ("Q3", .75), ("최대", 1)]}}
                    for c in columns]
    dates = [datetime.fromisoformat(r["last_post"]).timestamp() for r in rows if r["last_post"]]
    distribution.append({"지표": "last_post (UTC)", "유효 작가 수": len(dates),
                         **{label: datetime.fromtimestamp(quantile(dates, q), timezone.utc).isoformat()
                            if dates else None for label, q in
                            [("최소", 0), ("Q1", .25), ("중앙값", .5), ("Q3", .75), ("최대", 1)]}})
    bb = metrics(s["artists"][EXCLUDED], medians)
    zero = [r["태그"] for r in rows if not r["posts"]]
    years = [{"연도": y, "게시물 수": sum(s["years"][y].values()), "점수 중앙값": medians[y]} for y in sorted(medians)]
    candidate_set = {r["태그"] for r in rows}
    pool_matches = len(candidate_set & pool)
    rank_matches = len(candidate_set & ranks.keys())
    provenance = {k: s[k] for k in ["version", "dataset_revision", "tag_revision", "tag_sha256", "completed",
                                   "rows", "deleted", "kept", "multi_artist", "started_at"]}
    provenance.update(finished_at=datetime.now(timezone.utc).isoformat(), year_baselines=years,
                      zero_post_artists=zero, bb_baalbuddy=bb, content_tags=sorted(CONTENT_TAGS),
                      user_sources=user_sources, pool_matches=pool_matches, rank_matches=rank_matches,
                      user_rank_correlations=comparisons,
                      python=sys.version, pyarrow=__import__("pyarrow").__version__, requests=requests.__version__,
                      script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (output / "provenance.json").write_text(json.dumps(provenance, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = f"""# 단부루 아티스트 게시물 지표 — 후보 5,000명 (B-008 수정)

확인 수준: **실측**. 43개 Parquet 전체를 새로 집계했다. 이 표는 게시물의 점수·일반 태그·등급 분포를 나타내며, 작가의 품질이나 사용자의 취향을 판정하는 표가 아니다.

## B-008 반영과 사용 범위

- 플래그는 **흑백만화비중높음**(low_ratio ≥ 0.5)과 **표본부족**(posts < 30)만 사용한다. 이름은 실제로 측정한 내용에 맞췄다.
- `{CONTENT_COL}`은 `mature_female` 또는 `shiny_skin`을 포함한 게시물 비율이다. `realistic`은 제외했다. 기존 세 태그의 합집합 수에서 차감한 값이 아니라 원본 일반 태그를 다시 읽어 계산한 값이다.
- 이 열은 그 작가가 무엇을 자주 그렸는지에 대한 내용 태그 비율이며 취향 지표가 아니다. 새로운 취향 점수·추천 플래그·선별 순위는 만들지 않았다.
- 작업 기준으로 STATUS, D-005, D-006과 EXP-02 결과 1을 확인했다. D-006의 방향은 애니메 그림체 위의 광택과 강한 명암이며, 반실사 선호를 뜻하지 않는다. 실제 선택과의 관련성은 아래 절에서 별도로 확인한다.
- 단부루 posts는 이 데이터셋의 게시물 수일 뿐, NovelAI의 해당 작가 학습량·인식 정확도를 직접 확인한 수치는 아니다.

## 데이터와 처리 범위

- 집계 완료(UTC): {provenance['finished_at']}
- 태그 목록: [danbooru.csv]({TAG_URL.format(TAG_REV)}), 2025-01-03 커밋 `{TAG_REV}`.
- 태그 CSV SHA-256: `{s['tag_sha256']}`
- 게시물: [{DATASET}](https://huggingface.co/datasets/{DATASET}/tree/{DATA_REV}/data), 고정 리비전 `{DATA_REV}`.
- 파일 {len(s['completed'])}개, 원본 합계 {sum(f['size'] for f in s['files']):,}바이트.
- 원본 행 수 {s['rows']:,}; 삭제 제외 {s['deleted']:,}; 비삭제 전체 게시물 {s['kept']:,}.
- 비삭제 created_at 범위(UTC): {s['first'].isoformat()} ~ {s['last'].isoformat()}.
- 복수 작가 태그 게시물 {s['multi_artist']:,}개. 각 작가에게 한 번씩 집계했다. 후보별 posts 합계 {sum(r['posts'] for r in rows):,}는 공동 태그로 중복될 수 있다.
- 지정된 7개 메타데이터 열만 읽었다. 원본 파일은 순차 다운로드·해시 검증·집계 후 삭제했다.
- 사용자 풀: [pool1_user.txt](../../experiments/EXP-02_StyleLab/pool1_user.txt), {len(pool)}명. 후보 5,000명과 겹치는 작가 {pool_matches}명, 표 밖 {len(pool - candidate_set)}명.
- 기존 EXP-02 설명·판정의 213명 표기와 별개로, 이번 입력 파일에서 직접 센 고유 이름은 {len(pool)}개다. 입력 파일을 임의로 줄이지 않았다. 문서와 파일의 수가 다른 이유는 미확인이다.
- 사용자 순위: [artist_ranks_200.csv](../../experiments/EXP-02_StyleLab/artist_ranks_200.csv), {len(ranks)}명. 후보와 연결된 작가 {rank_matches}명, 표 밖 {len(ranks.keys() - candidate_set)}명.
- 사용자 입력 파일 SHA-256: pool `{user_sources['pool1']['sha256']}`, ranks `{user_sources['ranks']['sha256']}`. 실행 시작 시 내용을 고정해 체크포인트에 보관했다.

## 계산 및 결합 규칙

- 후보는 태그목록 게시물수 내림차순 안정 정렬; 동률은 원본 행 순서다. `{EXCLUDED}` 제외 후 상위 5,000명을 유지한다.
- 일반 태그·작가 태그는 공백 분리 후 완전 일치다. 별칭 병합은 하지 않는다. 동일 게시물의 중복 작가 태그는 한 번만 센다.
- low_ratio: {', '.join(sorted(LOW))} 중 하나 이상 / 해당 작가 posts. 이는 흑백·만화·스케치 등의 비중이며 작품 완성도를 뜻하지 않는다.
- `{CONTENT_COL}`: {', '.join(sorted(CONTENT_TAGS))} 중 하나 이상 / 해당 작가 posts. 두 태그가 모두 있어도 분자는 한 번만 증가한다. `realistic`만 있는 게시물은 분자에 들어가지 않는다.
- score_norm: 작가와 무관하게 **모든 비삭제 게시물**의 같은 연도 점수 중앙값으로 게시물 점수를 나눈 뒤 작가별 평균. 작가·연도 점수 합을 이용한 대수적으로 같은 식을 사용했다. 연도는 원본 created_at 시간대의 달력 연도다.
- 정확한 점수 빈도표로 중앙값을 계산한다. 짝수 표본은 가운데 두 값의 평균이며, 근사·샘플링은 하지 않았다.
- 연도 중앙값이 0이면 해당 연도를 포함한 작가의 score_norm은 `미확인`이다. posts=0도 평균·중앙값·비율·날짜는 `미확인`이다. score_norm 미확인 {sum(r['score_norm'] is None for r in rows)}명.
- g/s/q/e는 각각 해당 등급 수 / posts(0~1). last_post는 비삭제 최신 created_at을 UTC ISO 8601로 표시한다.
- `pool1_포함`: 포함 1, 미포함 0. pool1의 쉼표 구분 이름은 앞뒤 공백을 제거하고 내부 공백을 `_`로 바꿔 태그와 연결한다. 별칭·유사 이름은 추측해 합치지 않는다.
- `평균_순위`, `상위40_등장`은 제공된 artist_ranks_200.csv 값을 그대로 결합하며, 연결되지 않으면 **빈칸**이다. 0회는 실제 0으로 유지한다. 평균 순위가 낮을수록 사용자가 더 높게 평가한 조합에 속했다.
- 사분위수는 유효 값만 사용한 `(n−1)×q` 위치의 선형 보간(Type 7)이다. 사용자 순위 열의 빈칸도 분포에서 제외한다. CSV는 UTF-8 BOM, 보고서 수치는 유효숫자 8자리다.

## 각 지표의 분포

{table(distribution, ['지표', '유효 작가 수', '최소', 'Q1', '중앙값', 'Q3', '최대'])}

## 사용자 선택과의 대조

**실측 — Spearman 순위 상관.** 후보 5,000명 중 사용자 평균 순위와 각 지표가 모두 있는 작가만 지표별로 연결했다. 동률은 평균 순위를 부여한 뒤 Pearson 상관을 계산한다. n은 게시물 수나 조합 수가 아닌 **연결된 작가 수**다. 제공된 평균_순위의 소수점 정밀도를 그대로 사용했으며 원래 조합 순위에서 다시 산출하지 않았다.

{table(comparisons, ['지표', 'Spearman_rho', 'n', '해석'])}

- 평균_순위는 낮을수록 좋다. 따라서 **양수는 지표가 클수록 사용자 순위가 나쁜 방향**, 음수는 좋은 방향이다. 방향을 뒤집어 해석하지 않는다.
- 크기 설명은 |rho|<0.1이면 거의 없음, 0.1~0.3 미만은 약함, 0.3~0.5 미만은 중간, 0.5 이상은 큼으로 통일했다. 이는 설명용 구간이며 통계적 유의성·예측 성능을 판정한 것이 아니다.
- 이 결과는 사용자 1명, 시드 하나, 작가 1~4명 혼합·서로 다른 가중치를 쓴 200조합에서 나온 작가별 요약과의 대조다. 같은 조합을 공유하는 작가끼리는 관측이 독립적이지 않고, 등장 횟수도 서로 다르다. 작가별 평균을 같은 가중치로 대조했으며 인과관계·개별 작가 화풍의 선호를 분리해 증명하지 않는다.
- 상위 5,000명 밖 작가는 이번 대조에 들어가지 않는다. 약한 상관을 강한 선별 근거로 바꾸지 않는다. 이 대조만으로 새로운 취향 지표를 만들지 않는다.

## 연도별 정규화 기준

{table(years, ['연도', '게시물 수', '점수 중앙값'])}

## 흑백만화비중높음

총 **{len(high_low)}명**. 아래는 데이터셋 posts 내림차순 상위 30명이다(동률은 후보 순위). 작품의 질에 대한 판정이 아니다.

{table(high_low[:30], ['순위', '태그', '게시물수_태그목록', 'posts', 'low_ratio', 'score_norm'])}

## 검증 결과

- 아티스트 태그 59,201개: 통과.
- 제외 후 1위 ebifurya(5,924), 5,000위 jiekuijiangshadaonijiamenkou(271), quasarcake 4,518위: 모두 통과.
- `{EXCLUDED}` 별도 검증: posts {bb['posts']:,}, low 태그 게시물 {s['artists'][EXCLUDED]['low']:,}, low_ratio {fmt(bb['low_ratio'])}. 후보 집합·분포·상관에서는 제외했다.
- 사용자 참고값인 2025년 3~4월 16개 표본과는 기간·표본이 다르다. 해당 16개 표본의 동일성은 미확인이다.
- 후보 중 posts=0: **{len(zero)}명**, {', '.join(zero) if zero else '없음'}. 표본부족 {sum(r['posts'] < 30 for r in rows)}명.
- 원본 행 수=삭제+비삭제, 전체 연도 빈도 합=비삭제, 각 작가의 점수·연도·등급 빈도 합=posts, 점수 빈도표의 합계=연도별 점수 합계: assert 통과.
- 각 원본 크기·LFS SHA-256·Parquet 행 수 검증 통과. 입력 파일 중복 키·범위 검증도 통과했다. 원본별 해시와 상관값 원정밀도는 `provenance.json`에 보존한다.

## 제약과 불확실한 점

- 일반 태그는 그림 내용과 형식의 대리 지표이며 화풍·완성도·선호의 직접 측정이 아니다. 태그 부재로 특성 부재를 확정할 수 없다.
- 태그목록과 게시물의 기준 시점이 다르며, 삭제·이름 변경·별칭·공동 태그가 게시물수 차이와 누락을 만들 수 있다. 이름 변경은 보정하지 않았다.
- 연도 중앙값 보정은 노출 기간·인지도·팬덤·등급 차이를 완전히 제거하지 않는다. 2025년은 4월 중순까지의 부분 연도다.
- 요청된 7개 열에는 id가 없어 원본 ID 중복 여부는 미확인이고 별도 중복 제거를 하지 않았다.
- score/fav와 last_post는 수집 시점 데이터다. 현재 활동 여부·실제 NovelAI 학습량·프롬프트 효과는 미확인이다.

## 재실행

[설치·실행·이어하기](../../scripts/ARTIST_METRICS.md). 버전 2는 내용 태그 정의가 달라 버전 1 체크포인트를 재사용하지 않는다. 사용자 결합 입력은 새 실행 시 읽고 이어하기에는 저장된 스냅샷을 사용한다.
"""
    (output / "REPORT.md").write_text(report, encoding="utf-8")
    print(json.dumps({"rows": s["rows"], "kept": s["kept"], "deleted": s["deleted"],
                      "zero_posts": zero, "high_low": len(high_low), "pool_matches": pool_matches,
                      "rank_matches": rank_matches, "correlations": comparisons}, ensure_ascii=False), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    root = Path(__file__).resolve().parents[1]
    parser.add_argument("--work-dir", type=Path, default=root / ".artist-metrics-work-v2")
    parser.add_argument("--output-dir", type=Path, default=root / "data/artists")
    parser.add_argument("--resume", action="store_true", help="Only use a trusted, locally generated checkpoint")
    parser.add_argument("--pool-file", type=Path, default=root / "experiments/EXP-02_StyleLab/pool1_user.txt")
    parser.add_argument("--ranks-file", type=Path, default=root / "experiments/EXP-02_StyleLab/artist_ranks_200.csv")
    args = parser.parse_args()
    args.work_dir.mkdir(parents=True, exist_ok=True)
    checkpoint = args.work_dir / "checkpoint.pkl"
    if args.resume:
        with checkpoint.open("rb") as inp:
            state = pickle.load(inp)
        assert (state["version"], state["dataset_revision"], state["tag_revision"]) == (VERSION, DATA_REV, TAG_REV)
    else:
        if checkpoint.exists():
            parser.error("Checkpoint already exists; use --resume or a different --work-dir")
        pool, ranks, user_sources = load_user_inputs(args.pool_file, args.ranks_file)
        raw = get(TAG_URL.format(TAG_REV)).content
        tags = candidates(raw)
        files = get(f"https://huggingface.co/api/datasets/{DATASET}/tree/{DATA_REV}/data").json()
        files = sorted((f for f in files if f["path"].endswith(".parquet")), key=lambda f: f["path"])
        assert [f["path"] for f in files] == [f"data/train-{i:05d}-of-00043.parquet" for i in range(43)]
        assert all(f.get("lfs", {}).get("oid") for f in files), "Missing source file hash"
        state = new_state(tags, hashlib.sha256(raw).hexdigest(), files)
        state["user_inputs"] = {"pool": pool, "ranks": ranks, "sources": user_sources}
        save_checkpoint(state, checkpoint)
    done = {f["path"] for f in state["completed"]}
    # If interrupted after checkpoint but before deletion, remove that completed input.
    for item in state["files"]:
        if item["path"] in done:
            (args.work_dir / Path(item["path"]).name).unlink(missing_ok=True)
            continue
        print(f"[{len(done)+1}/43] download {item['path']}", flush=True)
        path, digest = download(item, args.work_dir)
        before = state["rows"]
        parquet = pq.ParquetFile(path)
        for batch in parquet.iter_batches(batch_size=8192, columns=COLS):
            consume(state, batch.to_pydict())
        assert state["rows"] - before == parquet.metadata.num_rows
        parquet.close()
        state["completed"].append({"path": item["path"], "size": item["size"], "sha256": digest,
                                   "rows": state["rows"] - before})
        save_checkpoint(state, checkpoint)
        path.unlink()
        done.add(item["path"])
        print(f"[{len(done)}/43] complete; total rows={state['rows']:,}; kept={state['kept']:,}; source deleted", flush=True)
    user_inputs = state["user_inputs"]
    finish(state, args.output_dir, user_inputs["pool"], user_inputs["ranks"], user_inputs["sources"])


if __name__ == "__main__":
    main()
