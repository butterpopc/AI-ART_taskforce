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
