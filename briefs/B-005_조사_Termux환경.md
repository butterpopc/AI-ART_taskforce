# B-005 조사 지시서 — 안드로이드 Termux에서 Python 앱 실행 환경 (→ R-002)

- 작성: 컨트롤 타워 · 2026-10-28
- 담당: **Gemini (조사)**
- 제출: RULES.md 2-1 **[조사 보고]** 양식, 보고 번호 **R-002**
- 배경: NAI Style Lab(Python 앱)을 개조해 **안드로이드 폰 한 대에서** 서버를 돌리고 같은 폰의 브라우저로 쓰려 한다 (PC 없이). 컨트롤 타워가 사용자용 설치 안내서를 쓰는데, 아래 사실들이 확인돼야 한다. 앱이 쓰는 것: Python 3(표준 라이브러리 http.server, ssl, threading), **Pillow**, 인터넷(HTTPS)으로 NovelAI API 호출, 폰 저장공간에 PNG 저장.

## 조사 항목 (항목마다 출처 링크 + 확인 수준)

1. **Termux 설치 경로**: 현재 권장 설치처(F-Droid / GitHub 릴리스 / Google Play). Play 스토어판의 현재 상태(정상 지원인지, 제한이 있는지). 최신 안정 버전과 날짜
2. **Python 설치**: `pkg install python` 시 설치되는 Python 버전 (2026년 기준)
3. **Pillow 설치 방법**: Termux 저장소에 `python-pillow` 패키지가 있는지. 없거나 안 되면 `pip install pillow`에 필요한 선행 패키지(libjpeg-turbo 등). 2026년 기준 알려진 문제
4. **HTTPS 인증서**: Termux의 Python이 기본 상태로 HTTPS 사이트에 접속할 때 인증서 오류가 나는지, 나면 해결법(ca-certificates 등)
5. **백그라운드 유지**: 화면을 끄거나 다른 앱(브라우저)으로 전환했을 때 Termux 프로세스가 죽지 않게 하는 방법 — `termux-wake-lock`, 알림 유지, 안드로이드 배터리 최적화 해제. **삼성 갤럭시(One UI)** 의 "앱 절전/잠자는 앱" 설정 위치를 특히 자세히
6. **저장소 접근**: `termux-setup-storage`로 휴대폰 '다운로드' 폴더의 zip을 Termux로 가져오는 방법과 경로 (`~/storage/downloads` 등)
7. **로컬 접속**: Termux에서 `127.0.0.1:포트`로 띄운 서버에 같은 폰의 Chrome으로 접속할 때 알려진 제약 (포트 번호 제한 등)
8. **안드로이드 버전 제약**: 최신 Termux가 요구하는 최소 안드로이드 버전, 안드로이드 12 이상의 "phantom process killer" 문제가 아직 있는지와 대처법

## 제약

- 링크는 실제로 연 것만. 공식(Termux GitHub/위키/F-Droid) 출처를 우선, 커뮤니티 출처는 표시
- 날짜가 중요한 정보(버전, 지원 상태)는 확인일과 함께
- 사용자 폰 기종은 미확인. 삼성 기준으로 쓰되 다른 제조사 차이는 짧게
- 한국어로 작성

## 완료 기준

- [ ] 8개 항목 모두 답 또는 "찾지 못함"
- [ ] [조사 보고] 양식 준수
