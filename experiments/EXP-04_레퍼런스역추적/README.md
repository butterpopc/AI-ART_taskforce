# EXP-04 레퍼런스 역추적 (사용자 자료실 그림의 숨은 프롬프트)

- 날짜: 2026-11-01 · 작성: 컨트롤 타워
- 사용자가 인터넷에서 모은 "마음에 드는 그림" 6장(PC 자료실 폴더). 이미지는 저장소에 올리지 않는다.
- 6장 모두 NovelAI가 그림 투명도 채널에 숨겨 넣는 정보(stealth_pngcomp)가 남아 있어 **프롬프트·설정을 그대로 읽음 (실측)**

## 모델
| 그림 | 모델 | 비고 |
|---|---|---|
| 1, 3, 4, 6 | **V5** | D-001에 따라 우리는 V4.5 사용 → 그대로 옮겨지지 않을 수 있음 (추정) |
| 2 (청록 머리 — 사용자가 "ㅈㄴ 예쁘다"고 한 그림), 5 | **V4.5 Full** | 바로 재현 시험 가능 |

## V4.5 레시피 (작가 부분)
- **그림 2:** `artist: kanpa (campagne 9), artist:danimaru, artist:quasarcake, artist:kim eb, 1.5::artist:wanke ::, artist:dfm (darknessdfm), realistic` · 28 steps · Guidance 5 · Rescale 0 · k_dpmpp_2m_sde / karras
- **그림 5:** `0.2::blue gk, 0.01::toma (toma50), 0.5::ciloranko, 0.7::teshima nari, 0.9::ratatatat74, 1.1::tokiame, 1.3::healthyman, 1.4::wanke, 1.45::akakura, 1.6::yoya yogurt, 1.65~1.7::bm94199, 1.4::azz0422, 0.8::kakure eria` + `ballpoint pen (medium), sketch, manga style` · 26 steps · Guidance 5 · k_euler_ancestral

## V5 레시피 (참고)
- **그림 4·6 (같은 작가 묶음):** `0.7::re0n, 1.0::murata_yuusuke, 1.0::jo_shin_ogi, 1.0::inoue_kiyoshirou, 0.7::ttptt, 0.7::moda_(mo_da_3)` + `-2::shiny skin, glistening skin` (광택을 일부러 뺌 → 깔끔한 무광 느낌)

## 알게 된 것
1. 잘 나온 그림들은 **작가 6~14명을 가중치 0.01~1.7로 잘게 섞는다.** 그리고 공통으로 `-3~-6::artist collaboration::`(작가 혼합 티 억제), 연도 태그(`year 2025` 등), 강한 품질 태그를 쓴다.
2. 이 레시피 속 작가 대부분은 우리 단독 훑기(EXP-03)에 **들어 있었지만 사용자가 좋아요를 주지 않았다** (kanpa, danimaru, wanke, healthyman, akakura 등). → **한 명씩 볼 때 평범한 작가도 섞으면 좋아질 수 있다.** 단독 훑기만으로 거르는 방식의 한계 (추정)
3. 우리 실험 프롬프트(P-003)는 단색 배경·정면 상반신이라 조명·배경·구도에서 오는 매력이 빠진다.

## 다음 (제안)
- 그림 2·5의 V4.5 레시피를 **우리 시험 캐릭터 프롬프트로 바꿔** 몇 장 그려 보고, 그림체가 살아남는지 확인

## 3D 단계 참고용 (사용자 지시, 2026-11-01)
- **그림 3 (V5):** 작가 `0.5::ebora, 0.6::geulimykun (skbyunea413), 0.8::shinjiro, 0.6::wagashi (dagashiya), 0.8::freng, 0.9::toma (toma50), 1::dkclaude3d, 1::takano suzu` + 렌더 태그 `3::cel rendering, 2::4k texture, 3d, 5::ray tracing, raytraced, 1.25::blender (medium), Zbrush (Medium)` · 23 steps · Guidance 7 · Rescale 0.4 · k_euler_ancestral
- 사용자: "3D화 할 때 참고하면 좋겠다". 2D 그림체를 3D 렌더 느낌으로 옮기는 태그 묶음으로 활용 (로드맵 4단계)

## 추가 2장 (2026-11-01 22시, 둘 다 V5)
- **그림 7 (흰 머리 안드로이드, 선화 위주·거의 무채색):** `0.5::henriiku (ahemaru), 0.4::shexyo, 0.5::geulimykun (skbyunea413), 0.6::wagashi (dagashiya), 0.6::pumpkinspicelatte, 0.3::fellatrix, 0.7::seoyong, 0.4::kunaboto, 0.4::kafun, 0.6::poper (arin sel), 0.55::blue gk, 0.8::toma (toma50), 1::takano suzu` + `2::flat color` · 23 steps · Guidance 7 · Rescale 0.4 · k_euler_ancestral
- **그림 8 (갈색 긴 머리 뒷모습, 창가 역광·수채 느낌):** `0.9::blue_gk, 0.6::eleaaa, 0.5::nixeu, 0.3::freng, 0.2::wlop, 0.9::bm94199, 0.3::matanonki, 0.6::greem_bang, 0.3::inushima, 0.4::marushin_(denwa0214), 'o'ne, zon_lee_sean, xi_xeong, 0.8::takaman_(gaffe)` · 23 steps · Guidance 7 · Rescale 0 · k_euler_ancestral

## 여러 레시피에 반복해서 나오는 작가 (8장 기준, 실측)
| 작가 | 나온 그림 수 |
|---|---|
| blue gk | 3 (가중치 0.2~0.9) |
| toma (toma50) | 3 (0.01~0.9) |
| takano suzu · geulimykun · wagashi (dagashiya) · freng · bm94199 · healthyman · wanke · ebora | 각 2 |
→ 커뮤니티에서 "받침용"으로 자주 섞는 작가로 추정. 단독 훑기에서 좋아요는 없었음

## garloo (사용자 제보, 2026-11-01)
- 커뮤니티 평: "단독으로 좋다" (미확인 전언)
- 받은 그림의 숨은 프롬프트(실측): **V5**, `artist:garloo` 단독 + `animated, promotional art, novel illustration, transparent background` · 28 steps · Guidance 5 · Rescale 0 · k_euler_ancestral
- 인상(추정): 굵고 깔끔한 외곽선, 단순한 셀 칠, 스티커풍 흰 테두리 → 사용자가 고른 "2번 무리(깔끔한 셀)"와 같은 방향
- **우리 작가 풀(4,516명)에 없던 작가** → V4.5 + 시험 캐릭터 프롬프트로 단독 1장, shiseki_hirame와 2명 조합으로 시험 예정

## 비교 메모 (2026-11-01, 추정)
- 사용자가 가장 좋아하는 건 그림 2(청록). 4장 공통 매력은 디테일·분명한 빛·표정·구도이고, 선 깔끔함·광택 정도는 제각각
- 우리 시험 프롬프트(P-003: 단색 배경·정면·옅은 미소)는 이 매력이 나올 수 없는 구조 → 1단계 마무리 때 "장면 3개 × (그림 2 레시피 / 핵심 3인방 / 섞음)" 비교 제안. 사용자: 일단 보류, 하던 작업 먼저
