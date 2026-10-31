# P-003 NAI Style Lab 공통 실험 환경 (P-002 대체)

- 작성: 컨트롤 타워 · 2026-10-27 · 요청: "적당히 예쁘게 나오는 공통 프롬프트"
- 용도: [T-001](../tools/T-001_nai-style-lab.md) NAI Style Lab의 모든 대결 (1차 풀: [POOL1](../experiments/EXP-02_StyleLab/POOL1_사용자목록.md))
- P-002와 차이: 비교에 방해되지 않는 선에서 **보기 좋은 구도·외형**을 넣음. 화풍을 덮어쓰는 태그(`realistic`, `shiny skin`, 조명·채색 태그)는 **일부러 뺌** — 작가 차이가 보여야 하므로

## 베이스 프롬프트

```
{artist}, 1girl, solo, upper body, looking at viewer, head tilt, simple background, grey background, very aesthetic, masterpiece, no text
```

## 캐릭터 1 프롬프트

```
girl, mature female, long hair, wavy hair, black hair, hair over shoulder, swept bangs, red eyes, half-closed eyes, light smile, closed mouth, lips, earrings, black dress, off-shoulder dress, bare shoulders, collarbone
```

## 캐릭터 1 네거티브

비워 둔다.

## 네거티브

```
lowres, artistic error, film grain, scan artifacts, worst quality, bad quality, jpeg artifacts, very displeasing, chromatic aberration, dithering, halftone, screentone, multiple views, logo, too many watermarks, negative space, blank page, @_@, mismatched pupils, glowing eyes, bad anatomy, signature, artist name, blurry, nsfw
```

## 설정

| 항목 | 값 | 근거 |
|---|---|---|
| 모델 | **V4.5 Full** | D-001, 무료 범위 (FACTS N8) |
| 크기 | 세로 832×1216 | Normal 크기 (FACTS N8) |
| Steps | 28 | 무료 상한 |
| 샘플러 | k_euler_ancestral (도구 기본) | — |
| Guidance(CFG) | **6** | 채널 V4.5F 실사용 조합들이 5~8 사용 ([모음집](https://arca.live/b/aiart/160585885), 게시글 확인). 그 중간값 — 추정 |
| CFG Rescale | **0.2** | 같은 글들이 0~0.6 사용. 낮은 쪽 — 추정 |
| 시드 | 고정. 후보 **3561572116** / 2049535591 / 3644369812 중 1개 (2026-10-27 무작위 생성) | 시드 값 자체에 좋고 나쁨은 없음. 구도가 무난한 것 하나를 골라 끝까지 고정 |

## 태그 선택 근거

- 모든 태그는 Danbooru 태그 목록(`danbooru.csv`)에 존재 확인. 예외: `nsfw`는 Danbooru 태그가 아님(등급은 별도 체계) — 커뮤니티에서 네거티브로 흔히 쓰지만 효과는 **미확인**
- 인원수(`1girl`)는 베이스, 캐릭터 칸은 숫자 없이 `girl` (공식 문서, 문서 확인)
- 외형(검은 웨이브 장발, 붉은 눈, 반쯤 뜬 눈, 오프숄더 검은 드레스): [D-005](../decisions/D-005_취향방향.md)(성숙미)를 반영한 **비교용 임시 외형**. 어깨·쇄골·입술은 피부 광택·입체 표현이 드러나는 부위 (추정). 실제 자캐 외형 아님
- 회색 배경: 흰 배경보다 피부 명암이 잘 보이고, 배경 묘사 차이로 비교가 흐려지는 것을 막음 (추정)
- `head tilt`: 정면 증명사진 느낌을 줄이는 최소한의 포즈
- 뺀 것: 조명 태그(`soft lighting` 등은 Danbooru 목록에 없음), `shiny skin`/`realistic`(모든 작가를 같은 질감으로 덮어씀), 배경 묘사(작가마다 크게 달라져 비교 방해)

## 바꾸지 말 것

- 대결 도중 프롬프트·설정을 바꾸면 이미 매긴 순위와 새 그림의 조건이 달라진다
- 바꾼다면 도구의 **다시 그리기 → 전체**로 모든 그림을 같은 조건으로 다시 그린다 (순위는 유지, 그림만 교체 — 도구 README)

## 시드 고르는 법 (2026-10-27)

1. 작가 1명짜리 조합 하나로 후보 시드 3개를 각각 1장씩 뽑는다
2. 얼굴이 잘리거나 손·자세가 어색하지 않은, **구도가 무난한 시드**를 고른다 (예쁜 정도가 아니라 구도 기준)
3. 그 시드를 도구 설정에 넣고 대결 끝까지 바꾸지 않는다
4. 시드 하나에 유리한 조합이 생길 수 있으므로, 다듬기 끝의 **다른 시드 3개 확인**으로 보정한다 (도구 기능)

## 실제 적용값 확인 (2026-10-31, 컨트롤 타워)

사용자 state.json(10-31 09:39 사본)의 설정에는 Guidance·Rescale·Steps·대기 값이 저장돼 있지 않았다. 그래서 Style Lab 기본값이 쓰였다(코드 확인: `engine.py` 기본 설정): **Steps 28, Guidance 5.0, Rescale 0.0, 생성 간 대기 1.0초**. 위의 Guidance 6 / Rescale 0.2는 Style Lab 실험(EXP-02, EXP-03)에 **적용되지 않았다.** 모든 그림이 같은 값이라 서로 비교하는 데는 문제없으므로, 진행 중인 실험은 이 값 그대로 유지한다.
