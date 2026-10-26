# T-001 NAI Style Lab 검토

- 검토: 컨트롤 타워 · 2026-10-26 · 발견: 사용자
- 대상: [sdnwls/nai-style-lab](https://github.com/sdnwls/nai-style-lab) v4.1.5 (릴리스 10-21, 커밋 10-22)
- 방법: 소스 코드를 내려받아 **읽기만** 함 (실행하지 않음). 확인 수준은 항목별 표시.
- 상태: **조건부 채택 제안 — 사용자 결정 대기**

## 1. 무엇을 하는 도구인가 (README·코드 확인)

NovelAI 작가 태그 조합의 그림을 **둘씩 나란히 보여주고 마음에 드는 쪽만 고르게** 해서, Elo 점수로 순위를 매기는 Windows 앱.

| 단계 | 내용 |
|---|---|
| 준비 | API 키 입력, 작가 등록, 무작위 조합 생성 |
| 순위 결정 | 새 조합을 이진 탐색으로 순위표에 배치 (좌/우 선택) |
| 진화 | 상위 30% 조합의 작가·가중치를 섞고 바꿔 새 조합 생성 → 대결로 평가 |
| 다듬기 | 작가는 그대로, 가중치만 바꾼 변형과 대결. 조정 폭 ±0.3 → ±0.2 → ±0.1 |
| 완성 | 다른 시드 3개로 원본과 최종본 비교 → 최종 태그 복사 |

- **모든 그림을 시드 하나로** 그린다 → 우리 실험 원칙(조건 고정, 작가만 변경)과 같음
- 블라인드 모드: 작가명·점수를 가리고 그림만 보고 고름
- 프롬프트 뷰어: NovelAI PNG를 끌어놓으면 프롬프트·설정 표시

**프로젝트와의 관계:** 1단계(화풍 발견 → 작가 조합)를 거의 그대로 자동화한다. "고르는 눈"만 사용자 몫으로 남기는 구조라, 원하는 화풍을 말로 설명하기 어려운 현재 상황에 잘 맞는다 (추정).

## 2. 안전성 (코드 확인 — 전체 정밀 감사는 아님)

| 항목 | 확인 내용 | 수준 |
|---|---|---|
| 통신 대상 | `image.novelai.net` (생성·구독 조회), `api.github.com`·`github.com` (자기 저장소 업데이트 확인)만 발견 | 코드 검색으로 확인 (약 6,200줄 전체를 한 줄씩 감사하진 않음) |
| API 키 저장 | `data/api_key.txt`에 **평문** 저장 | 코드 확인 |
| 데이터 내보내기 | 내보내기 zip에 **API 키가 포함됨** | 코드 확인 |
| 업데이트 | GitHub 릴리스에서 받고 크기·SHA-256 확인 후 설치 | 코드 확인 |
| 배포 파일 | 릴리스 zip(내장 Python 포함)이 공개 소스와 동일한지 | **미확인** |
| 개발 이력 | 개인 개발자 1명, 이 저장소 기준 2026-10-04 시작, 커밋 12개 | 확인 |
| 이용약관 | NovelAI가 제3자 도구의 API 사용을 허용하는지 | **미확인** |

## 3. 우리 설정과 다른 기본값 (반드시 변경)

| 설정 | 도구 기본값 | 우리 기준 | 이유 |
|---|---|---|---|
| **모델** | **V5 Full** | **V4.5 Full** | D-001. V5는 Opus 사용량 한도 소모, 초과 시 Anlas 차감 (FACTS N8) |
| 품질 태그 | 없음 (끔) | 프롬프트에 직접 추가 | 도구는 품질 태그·UC 프리셋을 항상 끈 상태로 보냄 |
| 네거티브 | 도구 자체 목록 | Human Focus 목록 + 우리 추가분을 직접 입력 | 같은 이유 |
| 조합당 작가 수 | 4~8명 | 처음엔 1명 → 이후 2~3명 | 아래 사용 순서 참고 |
| 가중치 범위 | 0.8~1.8 | 처음엔 기본값 유지 | 추정 |
| 크기 | 세로 832×1216 | 그대로 | Normal 크기, Opus 무료 범위 (FACTS N8) |
| Steps | 28 | 그대로 | 28 이하 무료 범위 |
| 한 번에 장수 | 1장 (`n_samples: 1`) | 그대로 | 무료 조건 충족 (코드 확인) |

### 도구에 넣을 기본 프롬프트

`{artist}` 자리에 작가 조합이 들어간다. 끝의 4개는 NovelAI 웹의 품질 태그(V4.5 Full)를 손으로 넣은 것 (FACTS N10).

```
{artist}, 1girl, solo, mature female, upper body, looking at viewer, neutral expression, black hair, short hair, blue eyes, white shirt, simple background, white background, location, very aesthetic, masterpiece, no text
```

### 도구에 넣을 네거티브

Human Focus 프리셋(V4.5 Full) 목록 + 우리 추가분 (FACTS N18, P-001).

```
lowres, artistic error, film grain, scan artifacts, worst quality, bad quality, jpeg artifacts, very displeasing, chromatic aberration, dithering, halftone, screentone, multiple views, logo, too many watermarks, negative space, blank page, @_@, mismatched pupils, glowing eyes, bad anatomy, signature, artist name, nsfw
```

## 4. 제안하는 사용 순서

1. **실험 1을 도구로 진행:** "특정 조합 만들기"로 작가 1명짜리 조합 6개를 만든다.
   ```
   1.0::artist:ciloranko ::
   ```
   (atdan, lam (ramdayo), puuzaki puuna, ishikei, yd (orange maru)도 같은 방식). **블라인드 ON**으로 대결 → 6명 순위.
2. **혼합 탐색:** 상위 작가 + R-001 보류 후보(as109, piromizu, melon22)를 등록하고, 조합 규칙을 작가 2~3명으로 바꿔 무작위 조합 → 순위 → 진화.
3. **다듬기 → 완성:** 최종 태그를 컨트롤 타워에 전달 → 프롬프트(P-002)로 확정.

## 5. 사용 시 지킬 것

- 릴리스 zip은 **GitHub 릴리스 페이지에서만** 받는다.
- NovelAI API 토큰은 계정 비밀번호에 준하는 정보다. **`data/` 폴더와 내보내기 zip은 이 공개 저장소에 절대 올리지 않고, 어떤 AI에게도 보내지 않는다.**
- 결과 공유는 **순위표 스크린샷**이나 최종 태그 문자열로 한다.
- 실행 전에 설정에서 **모델이 V4.5 Full인지** 확인한다.

## 6. 판정

- **[판정]** 조건부 동의 (도입 여부는 사용자가 결정)
- **[이유]** 1단계 목적과 방법론이 일치하고, 손으로 6장 뽑아 합본하는 수고를 없앤다. 통신 대상도 NovelAI·GitHub뿐이었다. 다만 신생 개인 도구라 배포 파일 검증·이용약관은 미확인이다.
- **[확인 수준]** 기능·통신·키 저장은 코드 확인. 배포 파일 동일성·약관은 미확인.
- **[다음 할 일]** 사용자가 도입을 결정하면 → D-006 기록, B-001을 도구 방식으로 개정
