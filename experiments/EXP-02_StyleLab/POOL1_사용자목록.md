# 1차 풀 — 사용자 제공 작가 목록 (검증본)

- 기록: 컨트롤 타워 · 2026-10-27
- 출처: 사용자가 대화에 첨부한 목록 244줄 (2026-10-26 22:13). **원래 출처는 미확인** (사용자가 그림체를 직접 보고 고른 목록은 아님 — 사용자 확인)
- 검증 방법: [EXP-02 README](README.md)와 같은 두 목록(Danbooru 태그 `danbooru.csv`, NAI 작가 목록 `artist_list.txt`)과 대조. 게시물 수는 목록 작성 시점 기준이라 지금과 다를 수 있음
- 상태: 사용자가 NAI Style Lab에서 사용 중 (2026-10-26 밤부터)

## 요약

| 구분 | 수 |
|---|---|
| 원본 줄 수 | 244 |
| 중복 제거 후 | 242 |
| **권장 등록 (아래 붙여넣기용)** | **214** — 정상 167 + 약함 47 |
| 빼기 권장: 게시물 50건 미만 + NAI 목록 없음 | 15 |
| 빼야 함: 태그 오류 | 아래 표 |

## 붙여넣기용 (214명)

같은 내용이 [`pool1_user.txt`](pool1_user.txt)에도 있음. 앞 167명이 "정상", 뒤 47명(`maosen`부터)이 "약함".

```
gomzi, miito (meeeeton333), eonsang, murata yuusuke, some1else45, wanke, shigure s, yd (orange maru), sparrowl, mikozin, hiro (dismaless), modare, dayama, au (d elete), hungry clicker, mgong520, waisshu (sougyokyuu), blackbox (blackbox9158), dino (dinoartforame), tianliang duohe fangdongye, mx2j, minaba hideo, messikid, yomu (sgt epper), pochi (pochi-goya), misaka 12003-gou, mikazuchi zeus, ohisashiburi, keihh, wagashi (dagashiya), teshima nari, hyocorou, mika pikazo, sarcophage, chomoran, gogalking, imamura ryou, controlline3, ningen mame, ie (raarami), tarou2, john kafka, ratatatat74, qtian, freng, touzai (poppin phl95), kittew, sawarakajin, nishikujic, ciloranko, hirota tsuu, konya karasue, arikanrobo, nixeu, na tarapisu153, jonpei, creayus, namori, tab head, kokaki mumose, qiandaiyiyu, healthyman, sumiyao (amam), kat (bu-kunn), optionaltypo, ame (uten cancel), ixy, momomatang, houtengeki, yamamoto souichirou, songchuan li, takaman (gaffe), nemu (nora), yunsang, kimidake, shinjiro, mushiro (nijie728995), kidmo, monaim, hiramedousa, wlop, ama mitsuki, iuui, pottsness, kaoming, kim eb, quasarcake, torino aqua, dishwasher1910, cutesexyrobutts, henriiku (ahemaru), ask (askzy), pepper0, bluethebone, ainy, aoki (fumomo), wengwengchim, wakamatsu372, blue gk, horosuke, horikoshi kouhei, mamaloni, ribiadan, cogecha, honnryou hanaru, beudelb, kim hyung tae, kakure eria, furau, mdf an, hito komoru, kieed, sugano manami, ikuhana niiro, myowa, sigm@, mankai kaika, kazutake hazano, fumihiro, imigimuru, mochizuki kei, duoyuanjun, fujiyama, mian lang, endou okito, akakura, uekura eku, kyouda suzuka, phantom ix row, hanagata, beni shake, haru57928031, pomu (joynet), nishizawa, pentagon (railgun ky1206), hizuki yayoi, himura kiseki, tamanoi peromekuri, yukiu con, zero (miraichizu), misumi (macaroni), mo (mocopo), chuzenji, satou kibi, shigure ui, haruba negi, pic postcard, inotukuhito, wujurana, xia (ryugo), mikami mika, akiyama enma, muchi maro, kugimiya atsuki, sho bu 1116, poriuretan, satsuki (miicat), quan (kurisu tina), 5saiji, onono imoko, u35, amagai tarou, liduke, hakusai (tiahszld), xiayehongming, morikura en, dorontabi, maosen, duckchuni, zero q 0q, bm94199, kubo tite, 96yottea, kim hana, doremi (doremi4704), tenpanco, kazuho iwamoto, inoue kiyoshirou, kamiyama sumu, nagamerin, solipsist, sqloveraven, yknsugar, mikakami1e, fungi542, imai akira, himemura saki, nimuno (munimuni), sangsoo jeong, fugtrup, ushikani kassen, cola (gotouryouta), yoggi (stretchmen), channel (caststation), yuyuharu 1027, kamizuki shiki, wantan meo, hatsushiro mamimu, ouchi kaeru, shirousa, yanngoto, araragi ayune, nikumaru, yokoyari mengo, soborou, jacknife, nanno koto, takahashi rumiko, iizuka haruko, mikuni mizuki, nakamura hinata, aiamu iamu, sakura hanpen, movik
```

## 빼야 함 — 태그 오류 (확인)

| 원본 표기 | 문제 | 처리 |
|---|---|---|
| satsuki (miicat), liduke | 두 번씩 들어 있음 | 1개만 남김 |
| cola gotouryouta | 표기 오류 | `cola (gotouryouta)`로 정정해 위 목록에 포함 |
| beautiful gunbari | 작가가 아니라 **작품명** 태그 | 제외 |
| yuune (ayanepuna) | 작가가 아니라 **캐릭터** 태그 (그 캐릭터가 그려질 수 있음) | 제외 |
| oshi no ko style, kimi ni todoke style, meitantei conan style, bishoujo senshi sailor moon style | 작가 태그 아님 (`artist:` 형식 부적합) | 제외. 효과는 나중에 별도 시험 |
| qin ningshui buleng, chanoo artz, ssxssss 848, sakalgath, sano yuuto, irotenya, pyon-kti | 대조 목록에 없음 (최근 작가일 수 있음) | **미확인** — 일단 제외 |

## 빼기 권장 — 인식 매우 약할 가능성 (15명, 데이터 근거)

Danbooru 게시물 50건 미만이고 NAI 작가 목록에도 없음. 무작위 조합에 섞이면 그 조합은 사실상 나머지 작가만으로 그려져 대결 횟수만 소모될 가능성 (추정). 특히 아끼는 작가라면 "특정 조합 만들기"로 단독 1장을 먼저 시험.

| 작가 | Danbooru 게시물 |
|---|---|
| 87yanagi | 26 |
| needbee r | 27 |
| keto cactus | 32 |
| kimhiro | 33 |
| pluvium grandis | 36 |
| noah (0noah) | 36 |
| kezime | 37 |
| takssmask | 38 |
| yoya yogurt | 41 |
| ginniroya | 42 |
| akutami gege | 43 |
| milkychu | 44 |
| soeyumi | 45 |
| japtangtang2 | 46 |
| pablo uchida | 48 |

## 남겨둠 — 취향 방향(D-005)과 다를 수 있음 (컨트롤 타워 추정)

`namori`, `shigure ui`, `yokoyari mengo`, `haruba negi` (귀여운 쪽), `kubo tite`, `horikoshi kouhei`, `takahashi rumiko` (소년만화 펜선 쪽 만화가 — 위 목록에 포함), `akutami gege` (빼기 권장 목록에 이미 포함)

→ 화풍 설명이 추정이고 사용자도 그림을 아직 보지 않았으므로 **빼지 않는다.** 블라인드 대결 결과로 판단.

## 기존 풀과의 관계

- [README](README.md)의 컨트롤 타워 수집 풀(57명 + 채널 158명)은 **2차 투입 후보**로 둔다. 1차 순위가 잡힌 뒤 추가
