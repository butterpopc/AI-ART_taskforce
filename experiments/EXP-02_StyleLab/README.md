# EXP-02 NAI Style Lab 작가 풀

- 도구: [T-001](../../tools/T-001_nai-style-lab.md) · 프롬프트: [P-002](../../prompts/P-002_StyleLab_기본.md)
- 작성: 컨트롤 타워 · 2026-10-26
- 상태: **사용자 실행 중** (2026-10-26 밤~). **1차 풀은 [POOL1_사용자목록](POOL1_사용자목록.md)** — 아래 컨트롤 타워 수집 풀은 2차 투입 후보

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

---

## 추가 풀 — AI 그림 채널(아카라이브) 수집 (2026-10-26 21:30, 158명)

- 출처는 채널의 공개 글이다. **이번 그룹 분류는 "어느 글에서 나왔는가"이며 화풍 추정이 아니다.**
- 검증: 앞의 두 목록과 같은 방식으로 대조. 단, 아래 A-2는 V4.5F 실사용 조합에 들어 있었지만 목록에 없거나 게시물 수가 적은 작가다 (목록이 오래돼 빠졌을 수 있음 — 추정).
- 제외: 같은 채널의 "작가태그 비급서(사파)" 글([138156485](https://arca.live/b/aiart/138156485))은 작성자가 직접 NSFW 성향 작가 위주라고 밝혀 넣지 않았다. asanagi도 같은 이유로 제외.

### A-1. V4.5F 그림체 모음집에서 실제 조합에 쓰인 작가 — 목록 확인 (44명)

출처: [스압) 지금까지 만든 4.5F 그림체 모음집](https://arca.live/b/aiart/160585885) (2026-01-25). 그중 **물광(shiny skin) 조합**에 쓰인 작가: ohisashiburi, rusellunt, ningen mame, john kafka, gogalking, qiandaiyiyu (+ 기존 풀의 modare, kim hyung tae, 목록 미등재 karyln)

```
yamamoto souichirou, ohisashiburi, sheya, dishwasher1910, spacezin, do m kaeru, kenkou cross, mizuryu kei, sukja, rei (sanbonzakura), qys3, abandon ranka, kupa (jesterwii), torino aqua, gogalking, ratatatat74, kawacy, try (lsc), krekkov, beeeeen, ningen mame, kim eb, mx2j, danimaru, asura (asurauser), myabit, qiandaiyiyu, reoen, ssambatea, john kafka, fajyobore, kyo-hei (kyouhei), quasarcake, au (d elete), yoneyama mai, henriiku (ahemaru), iuui, healthyman, rolua, mameojitan, mebaru, rurudo, 33 gaff, wanke, rusellunt
```

### A-2. 같은 글에서 쓰였지만 목록 미등재·게시물 적음 (29명) — 인식 약할 수 있음

```
channel (caststation), mori taishi, rifleman1130, karyln, mizu cx, quezify, magotsuki (hurray), noyu, blackbox, haragaita i, seapall, nyte tyde, ao (ao0 0nemu), hanaseto, others (gogo-o), aoseagrass, sapysha, abae, gemi ningen, hiita (hitta 99), izuru (timbermetal), sho (sho lwlw), tekito midori, k.pumpkin, kkuem, yueepon, wagashi (dagashiya), j.k, dog-san, hyulla
```

### B. "shiny skin, realistic" 공통 프롬프트로 정리된 NAI 4.5 작가 목록 — 목록 확인 (73명)

출처: [nai4.5 작가 (개인저장용)](https://arca.live/b/aiart/146697860) (2025-08-31, 수정 2026-06-01). 공통 프롬프트에 `1.2::shiny skin, pastel colors, 1.2::realistic::`가 들어간 상태의 견본이었음. 귀여운 쪽 작가도 섞여 있음 (추정).

```
ebifurya, kanikama, usashiro mani, momoko (momopoco), meyoco, sakura oriko, massakasama, tandohark, murata range, hong (white spider), fuzichoco, ucmm, zankuro, daizu (melon-lemon), ateoyh, dsmile, pigeon666, yuri kyanon, alphonse (white datura), yomosaka, yuugen, mitsumomo mamu, sido (slipknot), onono imoko, sakura yuki (clochette), freng, terada tera, reeh (yukuri130), zuizi, amonitto, marumoru, nikichen, marushin (denwa0214), kamioka shun'ya, meiji ken, youta, maccha (mochancc), love cacao, tatami to hinoki, feral lemma, atoki, aoi ogata, kimishima ao, pikaole, tenobe, kotteri, ranf, kaoming, uenomigi, lasto, kuwashima rein, usagi nui, toi8, coa (chroo x), raikoart, coyucom, dk.senie, onineko, pokimari, miyuki ruria, jikuno, kaneni, captain yue, soresaki, same anko, ishida umi, kacyu, yazawa oke, mimelond, wengwengchim, watanabe tomari, littlebluemuffin, keepout, taowu (20809)
```

### C. "성숙한 분위기" 질문글·조합 공유글 — 목록 확인 (8명)

출처: [전체적으로 성숙한 분위기 잘 뽑히는 작가 태그 없을까요?](https://arca.live/b/aiart/122045654) (2024-11), [애용하는 작가그림체 조합](https://arca.live/b/aiart/111281544) (2024-07), [개인적인 작가 조합식_1](https://arca.live/b/aiart/108380279) (2024-06). 뒤의 둘은 V3 시절 글이라 V4.5에서도 같은지는 미확인.

```
kedama milk, ame (uten cancel), damda, oda non, 6 (yuchae), distr, moyori, eonsang, osiimi
```

### 추가 풀 반영 시 도구 설정 변경

- 전체 215명 → 조합 2~3명 × 50개면 한 번도 안 뽑히는 작가가 많다. **첫 무작위 조합 수를 100개로** (도구 허용 범위 1~200, 코드 확인). V4.5 Full·Opus 조건이면 무료 (FACTS N8)
- 순위가 쌓인 뒤 "작가 점수"가 0 근처에 몰린 작가는 아직 판단 재료가 부족한 것 (도구 README: 들어간 조합이 적으면 0에 가까움)

### 채널에서 얻은 참고 팁 (출처: [그림체 어떻게 해요? 총집편](https://arca.live/b/aiart/154204833), 커뮤니티 경험담 — 추정)

- 앞쪽 작가일수록 영향이 강하다: 앞=몸매·구도, 중간=채색·분위기, 뒤=눈·세부
- 게시물이 많은 작가는 순서와 상관없이 강하게 나온다
- 비슷한 작가 찾기: nax.moe(작가별 예시 모음), Kaloscope 분류기(그림을 넣으면 비슷한 작가 추정 — 정확하지 않음)

## 작가 풀 2 (2026-10-29)

[GPT 아티스트 지표](../../data/artists/REPORT.md)에서 **이미 등록된 작가(pool1), 흑백·만화 비중이 높은 작가, 표본이 부족한 작가만 빼고** 점수(score_norm) 순으로 정렬했다. 성인 등급으로는 거르지 않았다([RULES 8](../../RULES.md)). Style Lab의 작가 등록 칸에 그대로 붙여 넣는 형식(쉼표 구분, 밑줄 대신 공백)이다.
- [pool2_추가300.txt](pool2_추가300.txt): 점수 상위 300명
- [pool2_추가전체.txt](pool2_추가전체.txt): 조건에 맞는 전체 4,451명
