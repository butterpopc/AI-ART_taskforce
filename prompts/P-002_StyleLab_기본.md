# P-002 NAI Style Lab용 기본 프롬프트 세트

- 용도: [T-001](../tools/T-001_nai-style-lab.md) NAI Style Lab에서 작가 조합 비교 (실험 1 및 혼합 탐색)
- 모델: **V4.5 Full** (도구 기본값 V5 Full → 반드시 변경)
- 기반: [P-001 v2](P-001_화풍비교_기본.md)의 내용을 도구 입력칸(베이스 / 캐릭터 / 네거티브)에 맞게 나눈 것
- 작성: 컨트롤 타워 · 2026-10-26

## 베이스 프롬프트

```
{artist}, 1girl, solo, upper body, looking at viewer, simple background, white background, very aesthetic, masterpiece, no text
```

## 캐릭터 1 프롬프트

```
girl, mature female, black hair, short hair, blue eyes, white shirt, neutral expression
```

## 캐릭터 1 네거티브

비워 둔다.

## 네거티브

```
lowres, artistic error, film grain, scan artifacts, worst quality, bad quality, jpeg artifacts, very displeasing, chromatic aberration, dithering, halftone, screentone, multiple views, logo, too many watermarks, negative space, blank page, @_@, mismatched pupils, glowing eyes, bad anatomy, signature, artist name, nsfw
```

## 왜 이렇게 나눴나

| 위치 | 넣은 것 | 근거 |
|---|---|---|
| 베이스 | 작가(`{artist}`), 인원수(`1girl, solo`), 구도, 배경, 품질 태그 | 공식 문서: 베이스는 장면·스타일을 정하고, **인원수 태그는 항상 베이스에** (문서 확인) |
| 캐릭터 | `girl` + 외형·표정 | 공식 문서: 캐릭터 프롬프트엔 **숫자 없이 `girl`/`boy`/`other`** 와 외형 (문서 확인) |
| 네거티브 | Human Focus 프리셋 목록 + `signature, artist name, nsfw` | 도구가 UC 프리셋을 끈 채로 보내므로 손으로 넣음 (FACTS N18, 코드 확인) |

- 품질 태그: 웹의 V4.5 Full 품질 태그는 `location, very aesthetic, masterpiece, no text`인데(FACTS N10), **`location`은 뺐다.** 흰 배경과 충돌해 작가마다 배경이 달라질 수 있기 때문 (추정). 비교 조건을 단순하게 유지하는 쪽을 택함.
- 외형을 캐릭터 칸에 둔 이유: 나중에 자캐 외형을 정할 때 **캐릭터 칸만 바꾸면** 되고, 베이스(화풍·품질)는 그대로 둘 수 있다.
- 검은 단발·파란 눈·흰 셔츠는 **비교용 임시 외형**이다. 실제 자캐 외형이 아니다.
- `mature female`의 NovelAI 인식 여부는 **미확인**. 결과가 어려 보이는 쪽으로 쏠리면 컨트롤 타워에 알린다.

## 바꾸지 말 것

- 이 세트로 대결을 시작한 뒤에는 **중간에 프롬프트를 바꾸지 않는다.** 바꾸면 이미 매긴 순위와 새 그림의 조건이 달라진다 (도구 README: 다시 그리기 시 순위는 유지되고 그림만 바뀜).
- 바꿔야 한다면 컨트롤 타워와 상의 후 "다시 그리기 → 전체"로 모든 그림을 같은 조건으로 맞춘다.
