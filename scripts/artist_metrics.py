#!/usr/bin/env python3
"""Exact, sequential Danbooru artist aggregation. Python 3.10+; pyarrow, requests.

Only metadata is downloaded. Checkpoints are local pickle files: never resume
from a checkpoint supplied by somebody else. See ARTIST_METRICS.md.
"""
import argparse
from collections import Counter, defaultdict
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
TASTE = frozenset("shiny_skin realistic mature_female".split())
COLS = ["tag_string_artist", "score", "fav_count", "tag_string_general",
        "rating", "created_at", "is_deleted"]
HEADERS = ["순위", "태그", "게시물수_태그목록", "posts", "score_mean",
           "score_median", "score_norm", "fav_mean", "low_ratio", "taste_ratio",
           "g", "s", "q", "e", "last_post", "플래그"]
VERSION = 1


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
            "year_n": Counter(), "fav": 0, "low": 0, "taste": 0,
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
        low, taste = bool(LOW & gtags), bool(TASTE & gtags)
        for tag in matches:
            a = s["artists"][tag]
            a["n"] += 1
            a["scores"][score] += 1
            a["year_sum"][year] += score
            a["year_n"][year] += 1
            a["fav"] += fav
            a["low"] += low
            a["taste"] += taste
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
    row = {k: None for k in HEADERS[4:-1]}
    row["posts"] = n
    if not n:
        return row
    row.update(score_mean=sum(k * v for k, v in a["scores"].items()) / n,
               score_median=hist_median(a["scores"]), fav_mean=a["fav"] / n,
               low_ratio=a["low"] / n, taste_ratio=a["taste"] / n,
               last_post=a["last"].isoformat())
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


def finish(s, output):
    assert len(s["completed"]) == 43, "Refuse to publish partial results"
    assert s["rows"] == s["kept"] + s["deleted"]
    assert sum(sum(h.values()) for h in s["years"].values()) == s["kept"]
    medians = {y: hist_median(h) for y, h in s["years"].items()}
    rows = []
    for i, (tag, source_count) in enumerate(s["candidates"], 1):
        a = s["artists"][tag]
        assert sum(a["scores"].values()) == sum(a["year_n"].values()) == sum(a["rating"].values()) == a["n"]
        assert 0 <= a["low"] <= a["n"] and 0 <= a["taste"] <= a["n"]
        rows.append({"순위": i, "태그": tag, "게시물수_태그목록": source_count, **metrics(a, medians)})
    cutoff = quantile([r["taste_ratio"] for r in rows], .75)
    for r in rows:
        flags = []
        if r["low_ratio"] is not None and r["low_ratio"] >= .5:
            flags.append("낙서의심")
        if r["posts"] < 30:
            flags.append("표본부족")
        if r["taste_ratio"] is not None and r["taste_ratio"] >= cutoff and r["low_ratio"] < .2:
            flags.append("취향후보")
        r["플래그"] = ";".join(flags)
    output.mkdir(parents=True, exist_ok=True)
    with (output / "artist_metrics_top5000.csv").open("w", encoding="utf-8-sig", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows({k: "미확인" if v is None else v for k, v in r.items()} for r in rows)
    suspicious = sorted((r for r in rows if "낙서의심" in r["플래그"]), key=lambda r: (-r["posts"], r["순위"]))
    taste = sorted((r for r in rows if "취향후보" in r["플래그"]), key=lambda r: (-r["taste_ratio"], r["순위"]))
    columns = ["게시물수_태그목록", "posts", "score_mean", "score_median", "score_norm", "fav_mean",
               "low_ratio", "taste_ratio", "g", "s", "q", "e"]
    distribution = [{"지표": c, "유효 작가 수": sum(r[c] is not None for r in rows),
                     **{label: quantile([r[c] for r in rows], q) for label, q in
                        [("최소", 0), ("Q1", .25), ("중앙값", .5), ("Q3", .75), ("최대", 1)]}}
                    for c in columns]
    dates = [datetime.fromisoformat(r["last_post"]).timestamp() for r in rows if r["last_post"]]
    distribution.append({"지표": "last_post (UTC)", "유효 작가 수": len(dates),
                         **{label: datetime.fromtimestamp(quantile(dates, q), timezone.utc).isoformat()
                            if dates else None for label, q in
                            [("최소", 0), ("Q1", .25), ("중앙값", .5), ("Q3", .75), ("최대", 1)]}})
    bb = metrics(s["artists"][EXCLUDED], medians)
    zero = [r["태그"] for r in rows if not r["posts"]]
    undefined = sum(r["score_norm"] is None for r in rows)
    years = [{"연도": y, "게시물 수": sum(s["years"][y].values()), "점수 중앙값": medians[y]}
             for y in sorted(medians)]
    provenance = {k: s[k] for k in ["version", "dataset_revision", "tag_revision", "tag_sha256", "completed",
                                   "rows", "deleted", "kept", "multi_artist", "started_at"]}
    provenance.update(finished_at=datetime.now(timezone.utc).isoformat(), year_baselines=years,
                      taste_q3=cutoff, zero_post_artists=zero, bb_baalbuddy=bb,
                      python=sys.version, pyarrow=__import__("pyarrow").__version__,
                      requests=requests.__version__,
                      script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (output / "provenance.json").write_text(json.dumps(provenance, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = f"""# 단부루 아티스트 태그 품질 지표 — 후보 5,000명

확인 수준: **실측**. 아래 값은 43개 Parquet 전부를 읽어 계산했다. 작가의 실제 화풍·품질 또는 NovelAI 학습 여부를 판정한 결과는 아니다.

## 데이터와 처리 범위

- 집계 완료(UTC): {provenance['finished_at']}
- 태그 목록: [danbooru.csv]({TAG_URL.format(TAG_REV)}), 고정 리비전 `{TAG_REV}`. 요청한 2025-01-03 갱신본의 검증값과 일치한다.
- 태그 CSV SHA-256: `{s['tag_sha256']}`
- 게시물: [{DATASET}](https://huggingface.co/datasets/{DATASET}/tree/{DATA_REV}/data), 고정 리비전 `{DATA_REV}`.
- 처리 파일: {len(s['completed'])}개, 다운로드 원본 합계 {sum(f['size'] for f in s['files']):,}바이트.
- 원본 행 수 {s['rows']:,}; 삭제 제외 {s['deleted']:,}; 비삭제 전체 게시물 {s['kept']:,}.
- 비삭제 게시물의 created_at 범위(UTC): {s['first'].isoformat()} ~ {s['last'].isoformat()}.
- 비삭제 전체 중 작가 태그가 2개 이상인 게시물 {s['multi_artist']:,}개. 각 작가에게 1회씩 집계했다.
- 후보 작가별 posts 합계 {sum(r['posts'] for r in rows):,}. 공동 태그 게시물은 여러 작가에 속하므로 고유 게시물 수와 다르다.
- 지정된 7개 열만 읽었다. 이미지·URL·작성자 개인정보 열은 읽지 않았다.

## 계산 및 경계 규칙

- 태그목록 게시물수 내림차순의 안정 정렬; 동률은 원본 CSV 행 순서 유지. `{EXCLUDED}`를 제외한 상위 5,000명이며, 별칭 병합은 하지 않았다.
- 일반 태그와 아티스트 태그 모두 공백으로 분리한 **완전 일치**를 사용한다. 같은 게시물 내 중복 작가 태그는 1회만 센다.
- low_ratio: {', '.join(sorted(LOW))} 중 하나 이상 / 해당 작가 posts.
- taste_ratio: {', '.join(sorted(TASTE))} 중 하나 이상 / 해당 작가 posts. 여러 조건이 맞아도 분자는 1이다.
- score_norm: 삭제 제외 **전체 작가·작가 태그 없는 게시물까지 포함한** 같은 연도 점수 중앙값을 분모로 한다. 연도는 created_at에 기록된 시간대의 달력 연도다. 작가·연도별 점수 합 / 연도 중앙값을 합한 뒤 posts로 나눈다. 이는 게시물별 정규화 후 평균과 대수적으로 같다.
- 중앙값은 정확한 정수 점수 빈도표로 계산하며 짝수 표본은 가운데 두 값의 평균이다. 근사 분위수·샘플링은 쓰지 않았다.
- 분모가 0인 연도가 있으면 해당 연도 게시물을 가진 작가의 score_norm 전체를 `미확인`으로 둔다. score_norm 미확인 작가: {undefined}명.
- posts=0은 0으로 기록하되 평균·중앙값·비율·날짜는 `미확인`. 분포 계산에서 미확인 값만 제외하고 유효 작가 수를 함께 표시한다.
- 사분위수는 정렬한 유효 값의 위치 `(n−1)×q`에서 선형 보간한다(Type 7).
- 취향후보: taste_ratio ≥ Q3(**{fmt(cutoff)}**)이며 low_ratio < 0.2. 경계 동률 모두 포함하므로 정확히 1,250명을 강제하지 않는다. posts<30도 조건에 맞으면 표본부족과 취향후보를 동시에 표시한다.
- 낙서의심: low_ratio ≥ 0.5; 표본부족: posts < 30. 플래그는 세미콜론으로 구분한다.
- g/s/q/e는 각 등급 게시물 수 / posts, 0~1 비율이다. last_post는 가장 최근 created_at을 UTC ISO 8601로 표시한다.
- CSV는 UTF-8 BOM이고 수치는 Python의 float 왕복 표현으로 보존한다. 이 보고서 표만 가독성을 위해 유효숫자 8자리로 표시한다.

## 각 지표의 분포

{table(distribution, ['지표', '유효 작가 수', '최소', 'Q1', '중앙값', 'Q3', '최대'])}

## 연도별 정규화 기준

{table(years, ['연도', '게시물 수', '점수 중앙값'])}

## 낙서의심

총 **{len(suspicious)}명**. 아래는 데이터셋 posts 내림차순 상위 30명이다(동률은 후보 순위).

{table(suspicious[:30], ['순위', '태그', '게시물수_태그목록', 'posts', 'low_ratio', 'score_norm'])}

## 취향후보

총 **{len(taste)}명**. 아래는 taste_ratio 내림차순 상위 50명이다(동률은 후보 순위).

{table(taste[:50], ['순위', '태그', 'posts', 'taste_ratio', 'low_ratio', 'score_norm', '플래그'])}

## 검증 결과

- 아티스트 태그 59,201개: 통과.
- 제외 후 1위 ebifurya(5,924), 5,000위 jiekuijiangshadaonijiamenkou(271), quasarcake 4,518위: 모두 통과.
- 제외 작가 `{EXCLUDED}`를 별도 검증 대상으로 동일하게 집계: posts **{bb['posts']:,}**, low 태그 게시물 **{s['artists'][EXCLUDED]['low']:,}**, low_ratio **{fmt(bb['low_ratio'])}**. low_ratio ≥ 0.5: **{'예' if bb['low_ratio'] is not None and bb['low_ratio'] >= .5 else '아니오'}**. 후보 집합·분포·취향 임계값에서는 제외했다.
- 사용자 참고값(2025년 3~4월 16개 표본, 약 81%)은 기간·표본이 다르므로 전체 집계값과의 일치를 요구하지 않는다. 해당 16개 표본의 동일성은 미확인.
- 후보 중 posts=0: **{len(zero)}명**. 해당 태그: {', '.join(zero) if zero else '없음'}.
- 표본부족: **{sum(r['posts'] < 30 for r in rows)}명**.
- 전체 행 수=삭제+비삭제, 연도별 빈도 합=비삭제, 각 작가의 점수·연도·등급 빈도 합=posts: 코드 assert 통과.
- 다운로드한 각 파일의 크기와 LFS SHA-256을 검증했다. 파일별 해시·행 수는 `provenance.json`에 보존한다.

## 제약과 불확실한 점

- 요청된 low/taste 태그는 게시물 특성의 대리 지표다. monochrome·sketch는 완성도 낮음을 뜻하지 않고 mature_female은 인물 속성이며, 태그 부재는 해당 특성 부재를 입증하지 않는다. 플래그를 자동 탈락·품질 판정으로 해석하지 않는다.
- 태그목록과 게시물 데이터의 기준 시점이 달라 두 게시물수는 같지 않을 수 있다. 삭제 제외·태그 변경·별칭·공동 작업 태그도 차이에 영향을 준다.
- 태그명은 정확히 일치시켰으며 이름 변경·별칭에 의한 누락은 별도 보정하지 않았다. 공동 작업의 실제 기여도는 미확인이다.
- 연도 중앙값 보정은 사용자 지정 계산식이다. 게시 연도 내 노출 기간, 점수 분포 변화, 작가 인지도·등급·팬덤 차이를 제거한다는 보장은 없다. 2025년은 4월 중순까지의 부분 연도다.
- 원본에 중복 게시물이 존재하는지는 미확인이다. 요청한 7개 열에 id가 없어 별도 ID 중복 제거를 하지 않았다.
- score/fav는 데이터셋 수집 시점의 값이며 현재 실시간 값이 아니다. 실제 그림의 광택·입체감·성숙함, 프롬프트 효과는 미확인이다.
- last_post는 비삭제 데이터셋 내 최신 게시물 날짜이지 현재 활동 여부가 아니다.

## 재실행

설치·실행·이어하기는 [scripts/ARTIST_METRICS.md](../../scripts/ARTIST_METRICS.md) 참고. 재현용 스크립트와 실행 환경·출처 해시는 저장소에 함께 제공한다.
"""
    (output / "REPORT.md").write_text(report, encoding="utf-8")
    print(json.dumps({"rows": s["rows"], "kept": s["kept"], "deleted": s["deleted"],
                      "zero_posts": len(zero), "suspicious": len(suspicious), "taste": len(taste),
                      "taste_q3": cutoff, "bb": bb}, ensure_ascii=False), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    root = Path(__file__).resolve().parents[1]
    parser.add_argument("--work-dir", type=Path, default=root / ".artist-metrics-work")
    parser.add_argument("--output-dir", type=Path, default=root / "data/artists")
    parser.add_argument("--resume", action="store_true", help="Only use a trusted, locally generated checkpoint")
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
        raw = get(TAG_URL.format(TAG_REV)).content
        tags = candidates(raw)
        files = get(f"https://huggingface.co/api/datasets/{DATASET}/tree/{DATA_REV}/data").json()
        files = sorted((f for f in files if f["path"].endswith(".parquet")), key=lambda f: f["path"])
        assert [f["path"] for f in files] == [f"data/train-{i:05d}-of-00043.parquet" for i in range(43)]
        assert all(f.get("lfs", {}).get("oid") for f in files), "Missing source file hash"
        state = new_state(tags, hashlib.sha256(raw).hexdigest(), files)
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
    finish(state, args.output_dir)


if __name__ == "__main__":
    main()
