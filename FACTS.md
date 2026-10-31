# FACTS — 확인된 사실 모음

> 실무 AI는 재조사 전에 여기부터 확인하세요. 각 항목에 확인 수준·확인일·출처를 적습니다.
> 서비스 사양은 바뀔 수 있으므로, 확인일이 오래됐으면 재확인 후 갱신합니다.

## NovelAI

| # | 사실 | 확인 수준 | 확인일 | 출처 |
|---|---|---|---|---|
| N1 | **Precise Reference는 V4.5 모델 전용.** Vibe Transfer와 동시 사용 불가 | 문서 확인 | 2026-10-26 | [Precise Reference](https://docs.novelai.net/en/image/precisereference/) |
| N2 | Precise Reference 사용 시 **생성 1장당 5 Anlas 추가**, 참조 이미지 수에 비례해 증가 | 문서 확인 | 2026-10-26 | 같은 문서 |
| N3 | Precise Reference 종류: Character / Style / Character & Style. 슬라이더: Strength, Fidelity | 문서 확인 | 2026-10-26 | 같은 문서 |
| N4 | Character Reference용 이미지 권장: 단순 배경의 정면 전신, 중립 포즈, 깔끔한 그림. 구석에 얼굴 확대 추가하면 도움 | 문서 확인 | 2026-10-26 | 같은 문서 |
| N5 | 참조 이미지는 항상 1024×1536 / 1472×1472 / 1536×1024 중 하나로 맞춰짐 (작으면 확대, 크면 축소 + 여백) | 문서 확인 | 2026-10-26 | 같은 문서 |
| N6 | 다각도 참조용 시트 생성에 유용한 태그: `multiple views`, `turnaround`, `reference sheet`(+`no text`), `expressions` | 문서 확인 | 2026-10-26 | 같은 문서 |
| N7 | V5에서는 Precise Reference·Vibe Transfer가 아직 비활성(출시 시점 기준). V5의 강점은 다인원 배치, 투명 배경 | 문서 확인(제3자 정리) | 2026-10-26 | [weavai 정리](https://weavai.app/blog/zh-cn/2026/08/29/novelai-diffusion-v5%E4%B8%8A%E7%BA%BF%EF%BC%9A22%E4%BA%BA%E5%90%8C%E6%A1%86%E4%B8%8E%E5%8E%9F%E7%94%9F%E6%8A%A0%E5%9B%BE/) |
| N8 | **Opus 무료 생성 조건:** 한 번에 1장, 베이스 이미지 없음, Normal 크기 이하(약 1024×1024), Steps 28 이하. **V4.5 이하 모델만 사실상 무제한**, 그보다 상위 모델은 사용량 한도 초과 시 Anlas 소모 | 문서 확인 | 2026-10-26 | [Subscription](https://docs.novelai.net/en/subscription) |
| N9 | Opus는 매월 Subscription Anlas 10,000 충전 (미사용분만큼만 채워짐) | 문서 확인 | 2026-10-26 | 같은 문서 |
| N10 | V4.5 Full에서 Add Quality Tags를 켜면 프롬프트 끝에 `, location, very aesthetic, masterpiece, no text` 자동 추가 | 문서 확인 | 2026-10-26 | [Add Quality Tags](https://docs.novelai.net/en/image/qualitytags/) |
| N11 | 수치 가중치 문법 `1.5::태그 ::` (V4 이상). 0~1 사이는 약화. **혼합 비율이 아니라 각 태그의 영향력**이며 합이 1일 필요 없음. 음수 가중치는 V4.5 이상 | 문서 확인 | 2026-10-26 | [Strengthening & Weakening](https://docs.novelai.net/en/image/strengthening-weakening) |
| N12 | `{ }` = ×1.05 강화, `[ ]` = ÷1.05 약화, 중첩 시 곱해짐 | 문서 확인 | 2026-10-26 | 같은 문서 |
| N13 | NovelAI는 외부 LoRA를 불러올 수 없음 | 추정(여러 출처 일치, 공식 문구 미확인) | 2026-10-26 | — |
| N14 | V4/V4.5는 **T5 토크나이저**, 기본+캐릭터 프롬프트 합계 **약 512 T5 토큰**. 이모지·일본어 등 대부분의 유니코드 문자는 프롬프트로 지원 안 됨 → **영문 태그만** | 문서 확인 | 2026-10-26 | [Models](https://docs.novelai.net/en/image/models) |
| N15 | 자동완성은 태그 제안과 함께 **모델이 그 태그를 얼마나 아는지 표시(marker)** 를 보여줌 → 작가 태그 인식 여부 판단에 사용 | 문서 확인 | 2026-10-26 | [Tagging](https://docs.novelai.net/en/image/tags) |
| N16 | Danbooru 태그의 밑줄은 NovelAI 입력에서 **공백**으로 쓴다 (`puuzaki_puuna` → `puuzaki puuna`). 소문자 권장 | 문서 확인(제3자) — Gemini R-001, 컨트롤 타워 재확인 불가 | 2026-10-26 | [R-001](research/R-001_작가태그조사.md) |
| N16-상충 | NAI Style Lab은 공백을 **밑줄**로 바꿔 보낸다 (`artist:puuzaki_puuna`). 개발자는 "NovelAI가 받는 형태"라고 주석에 적었고 웹과 같은 그림이 나온다고 주장. 공백/밑줄 둘 다 통하는지는 **미확인** | 코드 확인(도구), 효과 미확인 | 2026-10-26 | [T-001](tools/T-001_nai-style-lab.md) |
| N17 | `artist:name`과 `artist: name`(콜론 뒤 공백)은 같은 결과 | 커뮤니티 실험 — Gemini R-001, 재확인 불가 | 2026-10-26 | 같은 문서 |
| N18 | UC 프리셋(V4.5 Full): **Heavy** = lowres, artistic error, film grain, scan artifacts, worst quality, bad quality, jpeg artifacts, very displeasing, chromatic aberration, dithering, halftone, screentone, multiple views, logo, too many watermarks, negative space, blank page / **Light** = Heavy보다 적은 목록 / **Human Focus** = Heavy + @_@, mismatched pupils, glowing eyes, bad anatomy / **Furry Focus** 별도. 권장 프리셋은 기본으로 켜져 있음 | 문서 확인 | 2026-10-26 | [Undesired Content](https://docs.novelai.net/en/image/undesiredcontent) |
| N19 | 생성 요청을 쉬지 않고 연달아 보내면 NovelAI 서버가 **매크로로 판단해 응답을 거부**한다. NAI Style Lab v4.1.6은 그래서 생성 간 대기를 기본 **3~5초 무작위**로 늘렸다 → 대기를 0으로 줄이지 말 것 | 사용자 전달(원작자·커뮤니티 측 설명) + 코드 확인(4.1.6 기본값 delay 3.0, delay_max 5.0). NovelAI 공식 문서 미확인 | 2026-10-31 | [T-001](tools/T-001_nai-style-lab.md) |

## 작가 태그 인식 여부

| 작가 태그 (NovelAI 입력 표기) | Danbooru 원문 | 규모 (R-001, 재확인 불가) | NovelAI 인식 |
|---|---|---|---|
| `artist:ciloranko` | `ciloranko` | 2024-11 상위 2,000 밖 | 미확인 — 실험 1에서 자동완성 표시로 확인 |
| `artist:atdan` | `atdan` | 531위 | 〃 |
| `artist:lam (ramdayo)` | `lam_(ramdayo)` | 상위 2,000 밖 | 〃 |
| `artist:puuzaki puuna` | `puuzaki_puuna` | 1,372위 | 〃 (사용자 선호 작가) |

## ComfyUI / 로컬 (현재 보류 중, 참고용)

| # | 사실 | 확인 수준 | 비고 |
|---|---|---|---|
| C1 | "ComfyUI 최소 사양 12GB" 같은 공통 기준은 없음. 모델·해상도·기능 조합에 따라 다름 | 추정(GPT가 공식 문서 대조) | 2026-10-26 GPT 검토 |
| C2 | 현재 ComfyUI 공식 코드에 `--medvram` 옵션 없음. `--lowvram`은 동적 VRAM 관리 활성 시 효과 없음 | 미확인(GPT 주장, 컨트롤 타워 재확인 안 함) | 사용 시점에 재확인 |
| C3 | IP-Adapter + OpenPose ControlNet으로 **모든 각도의 완전 일치 보장 안 됨** (자세 유도·외형 참조일 뿐) | 추정 | — |
| C4 | TripoSR은 기본적으로 **단일 이미지 → 3D**. 여러 방향 시트를 통합 복원하는 모델이 아님 | 미확인(GPT 주장) | 사용 시점에 재확인 |

## 3D (현재 보류 중, 참고용)

| # | 사실 | 확인 수준 |
|---|---|---|
| T1 | VRoid Studio는 그림을 자동으로 3D로 바꾸지 않음. 원화를 보며 슬라이더·편집으로 직접 비슷하게 만드는 방식 | 추정(GPT 검토) |
| T2 | VRoid 모델 → VRM 내보내기 → VSeeFace 등 추적 프로그램 연결이 별도 단계 | 추정(GPT 검토) |
