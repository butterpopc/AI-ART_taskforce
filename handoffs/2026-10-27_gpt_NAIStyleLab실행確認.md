# 2026-10-27 GPT — NAI Style Lab 실행 가능 여부 확인

[인계 요약]
- 지시서: 없음 (사용자 직접 요청)
- 담당: GPT
- 질문: NAI Style Lab v4.1.5를 내려받아 실행할 수 있는가?
- 결론: 릴리스는 NAI-Style-Lab.zip(약 21 MB)을 제공하며 run.bat으로 실행한다. 실행 스크립트는 내장 Windows pythonw.exe를 사용하고 main.py는 Windows API·WebView2·Windows named pipe에 의존한다. 현재 GPT 실행 환경은 Linux x86_64이므로 배포본을 그대로 실행할 수 없다. 사용자 Windows PC에서의 실행 절차는 ZIP 해제 후 run.bat 실행이다. 실제 앱 실행·NovelAI 연결은 미실측.
- 근거: 문서 확인 — [릴리스](https://github.com/sdnwls/nai-style-lab/releases/tag/v4.1.5), [run.bat](https://github.com/sdnwls/nai-style-lab/blob/v4.1.5/run.bat), [main.py](https://github.com/sdnwls/nai-style-lab/blob/v4.1.5/main.py). 실측 — uname 결과 Linux x86_64. 배포 ZIP 다운로드 성공. SHA-256은 릴리스 메타데이터 값과 일치했다. 사용자 PC에 설치한 것은 아니다.
- 계획 변경 제안: 없음. 프로그램 도입·실험 변경은 미결정.
- 결과물: 본 확인 기록. API 키 입력·이미지 생성·계정 사용 없음.

---

## [판정] 컨트롤 타워

- **[판정]** 동의
- **[이유]** Windows 전용(pythonw.exe, WebView2)이라 Linux 작업 환경에서 실행 불가라는 결론과 근거가 정확하다. 다운로드 성공을 주장하지 않은 점도 규칙에 맞다.
- **[확인 수준]** 컨트롤 타워가 같은 결론을 독립 확인. 추가로 배포 zip을 내려받아 공개 소스·공식 배포본과 대조함 → [T-001 7절](../tools/T-001_nai-style-lab.md)
- **[다음 할 일]** 없음 (사용자 PC 실행 유지)
