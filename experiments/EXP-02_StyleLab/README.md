# EXP-02 NAI Style Lab 작가 풀

- 도구: [T-001](../../tools/T-001_nai-style-lab.md) · 프롬프트: [P-002](../../prompts/P-002_StyleLab_기본.md)
- 작성: 컨트롤 타워 · 2026-10-26
- 상태: **작가 등록 대기**

## 작가 선정 방식과 검증

- **후보 이름은 컨트롤 타워가 골랐다.** 기준은 [D-005](../../decisions/D-005_취향방향.md)(성숙미·입체적 광택)와 [EXP-00](../EXP-00_취향자료/README.md)(가는 선·눈 강조)에 가까울 것. 비교를 위해 다른 쪽 화풍도 일부 넣었다.
- **그룹 분류는 전부 추정이다.** 실제 판단은 도구에서 고르는 사용자의 눈으로 한다.
- **태그 존재는 두 목록으로 확인했다** (57명 전원 통과):
  - \* Danbooru 작가 태그 + 게시물 수: [a1111-sd-webui-tagcomplete `danbooru.csv`](https://github.com/DominikDoom/a1111-sd-webui-tagcomplete/blob/main/tags/danbooru.csv) — 제3자 자동완성 데이터. **목록 작성 시점의 수치**이며 현재 실제 수와 다를 수 있다 (작성 시점 미확인)
  - \*\* NovelAI용 작가 목록: [NAI-Prompt-Randomizer `artist_list.txt`](https://huggingface.co/Jio7/NAI-Prompt-Randomizer/blob/main/artist_list.txt) (12,200명) — 제3자 목록. NovelAI 공식 인식을 보장하지 않는다
- 제외 기준: 게시물 200건 미만이거나 NAI 목록에 없는 후보는 뺐다. (예: krenz 142건·목록 없음, zumi·hiten 등은 이 표기로 Danbooru에 없음)

### 1. 기존 후보 (실험 1 + R-001 보류)

| 작가 (도구 입력) | Danbooru 게시물 수* | NAI 목록** |
|---|---|---|
| ciloranko | 204 | ✅ |
| atdan | 905 | ✅ |
| lam (ramdayo) | 380 | ✅ |
| puuzaki puuna | 574 | ✅ |
| ishikei | 1656 | ✅ |
| yd (orange maru) | 1667 | ✅ |
| as109 | 1525 | ✅ |
| piromizu | 1099 | ✅ |
| melon22 | 818 | ✅ |

### 2. 광택·입체 / 반실사 쪽 (분류 추정)

| 작가 (도구 입력) | Danbooru 게시물 수* | NAI 목록** |
|---|---|---|
| sakimichan | 1014 | ✅ |
| wlop | 365 | ✅ |
| guweiz | 667 | ✅ |
| liang xing | 830 | ✅ |
| nixeu | 241 | ✅ |
| zaphn | 579 | ✅ |
| olchas | 326 | ✅ |
| sciamano240 | 919 | ✅ |
| kim hyung tae | 370 | ✅ |
| prywinko | 539 | ✅ |
| starshadowmagician | 829 | ✅ |
| nyantcha | 2260 | ✅ |
| ask (askzy) | 470 | ✅ |

### 3. 성숙미·섹시미 애니풍 (분류 추정)

| 작가 (도구 입력) | Danbooru 게시물 수* | NAI 목록** |
|---|---|---|
| tony taka | 3146 | ✅ |
| mizuki hitoshi | 4312 | ✅ |
| hews | 2579 | ✅ |
| houtengeki | 2359 | ✅ |
| toosaka asagi | 1888 | ✅ |
| cle masahiro | 1512 | ✅ |
| sky-freedom | 1302 | ✅ |
| kase daiki | 1203 | ✅ |
| shexyo | 686 | ✅ |
| afrobull | 1492 | ✅ |
| cutesexyrobutts | 1436 | ✅ |
| aztodio | 1092 | ✅ |
| kuroonehalf | 393 | ✅ |
| liduke | 376 | ✅ |

### 4. 선명한 애니 일러스트 — 가는 선·눈 강조 쪽 (분류 추정)

| 작가 (도구 입력) | Danbooru 게시물 수* | NAI 목록** |
|---|---|---|
| fkey | 1086 | ✅ |
| redrop | 861 | ✅ |
| mika pikazo | 993 | ✅ |
| lack | 1099 | ✅ |
| wada arco | 670 | ✅ |
| kishida mel | 1010 | ✅ |
| nardack | 878 | ✅ |
| tsunako | 2018 | ✅ |
| huke | 455 | ✅ |
| redjuice | 418 | ✅ |
| morikura en | 688 | ✅ |
| rella | 396 | ✅ |
| anmi | 634 | ✅ |
| tiv | 374 | ✅ |
| mochizuki kei | 554 | ✅ |

### 5. 분류 미정 (화풍을 확실히 모름)

| 작가 (도구 입력) | Danbooru 게시물 수* | NAI 목록** |
|---|---|---|
| sincos | 1988 | ✅ |
| modare | 832 | ✅ |
| torriet | 793 | ✅ |
| nekometaru | 363 | ✅ |
| oekakizuki | 1096 | ✅ |
| gweda | 1678 | ✅ |

## 붙여넣기용 (전체 57명)

```
ciloranko, atdan, lam (ramdayo), puuzaki puuna, ishikei, yd (orange maru), as109, piromizu, melon22, sakimichan, wlop, guweiz, liang xing, nixeu, zaphn, olchas, sciamano240, kim hyung tae, prywinko, starshadowmagician, nyantcha, ask (askzy), tony taka, mizuki hitoshi, hews, houtengeki, toosaka asagi, cle masahiro, sky-freedom, kase daiki, shexyo, afrobull, cutesexyrobutts, aztodio, kuroonehalf, liduke, fkey, redrop, mika pikazo, lack, wada arco, kishida mel, nardack, tsunako, huke, redjuice, morikura en, rella, anmi, tiv, mochizuki kei, sincos, modare, torriet, nekometaru, oekakizuki, gweda
```

## 도구에서의 사용법

- 작가 화면에 위 블록을 그대로 붙여넣는다. `artist:` 없이 쉼표로 나눈 이름 목록을 받으며, 공백은 도구가 밑줄로 바꿔 등록한다 (코드 확인)
- **도구 기본 작가 23명은 지운다.** 귀여운 쪽 화풍이 섞여 있어 D-005와 방향이 다르고, 일부는 NAI 목록에 없다 (확인)
- 조합 규칙: **조합당 작가 2~3명**, 가중치 범위는 기본값(0.8~1.8). 첫 무작위 조합은 기본 50개
- 대결은 **블라인드 ON**
- 작가 표의 "작가 점수"가 쌓이면 상위·하위 작가를 컨트롤 타워에 전달 → 다음 단계 판단

## 주의

- 3그룹 일부(afrobull, cutesexyrobutts, aztodio 등)는 노출 많은 그림 비중이 큰 작가다 (추정). 네거티브의 `nsfw`를 빼지 않는다.
- 결과 공유는 순위표·작가 점수 스크린샷으로. 생성 이미지 원본에는 프롬프트 메타데이터가 들어 있을 뿐 개인정보는 없지만, `data/` 폴더 자체는 올리지 않는다 (API 키 포함).
