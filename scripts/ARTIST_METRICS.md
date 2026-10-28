# 단부루 작가 게시물 지표 재실행 (B-008, 버전 2)

Python 3.10 이상(권장 64비트 Python 3.12), 인터넷 연결이 필요합니다. GPU·Hugging Face 로그인·유료 API는 사용하지 않습니다. 저장소 루트에서 실행합니다.

## Windows PowerShell

```powershell
py -3.12 -m venv .venv-artists
.\.venv-artists\Scripts\python.exe -m pip install -r scripts/artist_metrics_requirements.txt
.\.venv-artists\Scripts\python.exe -m unittest discover -s scripts -p test_artist_metrics.py -v
.\.venv-artists\Scripts\python.exe -u scripts/artist_metrics.py
```

## macOS / Linux

```bash
python3 -m venv .venv-artists
.venv-artists/bin/python -m pip install -r scripts/artist_metrics_requirements.txt
.venv-artists/bin/python -m unittest discover -s scripts -p test_artist_metrics.py -v
.venv-artists/bin/python -u scripts/artist_metrics.py
```

## 중단 후 이어하기

같은 명령 끝에 `--resume`을 붙입니다. 예:

```powershell
.\.venv-artists\Scripts\python.exe -u scripts/artist_metrics.py --resume
```

- 한 번에 원본 Parquet 하나만 내려받습니다. 총 전송량은 약 7.60GB이며 재시도하면 늘어납니다.
- 읽는 열은 지시된 7개뿐입니다. 8,192행 단위로 처리하고 이미지 파일은 내려받지 않습니다.
- 한 파일 집계를 마치면 합계·점수 빈도표를 체크포인트에 원자적으로 저장하고 해당 원본 Parquet를 바로 지웁니다.
- 진행 중 예외가 나면 결과 CSV/보고서를 새로 만들지 않습니다. 마지막으로 완료한 파일부터 이어받아 미완료 파일은 다시 처리합니다.
- 체크포인트는 기본 `.artist-metrics-work-v2/checkpoint.pkl`입니다. **직접 생성한 체크포인트만 사용하세요.** pickle은 외부에서 받은 파일을 열기에 안전한 형식이 아닙니다.
- 내용 태그 정의가 변경되어 버전 1 체크포인트는 재사용할 수 없습니다. 버전 2로 처음부터 집계해야 합니다.
- 처음부터 다시 계산하려면 새 작업 폴더를 지정합니다: `--work-dir .artist-metrics-work-new`.
- 결과 경로는 기본 `data/artists/`입니다. 기존 산출물을 유지하려면 `--output-dir 별도경로`를 지정합니다.
- 43개 파일 모두 완료해야 최종 결과를 출력합니다. 중간 집계값을 최종값처럼 사용하지 않습니다.

## 산출물과 재현 기준

- `data/artists/artist_metrics_top5000.csv`: UTF-8 BOM, 요청한 열 순서. 비율은 퍼센트 문자열이 아닌 0~1 수치입니다.
- `data/artists/REPORT.md`: 한국어 집계 보고서, 분포·연도별 분모·사용자 순위와의 상관·검증·제약.
- `data/artists/provenance.json`: 입력 리비전·해시, 파일별 행 수, 실행 환경, 검증용 제외 작가 결과, 사용자 파일 해시와 상관값.
- 소스는 고정 리비전입니다. 태그 목록 59,201명과 3개 순위 검증값이 달라지면 중단합니다. 후보 동률은 원본 순서입니다.
- 게시물별 점수를 모두 보관하는 대신 **정확한 점수별 빈도표**를 보관합니다. 중앙값은 근사가 아닙니다.
- 내용태그비율(mature_female·shiny_skin)은 두 태그 중 하나 이상 있는 게시물의 비율입니다. `realistic`은 포함하지 않습니다. 내용의 빈도이며 취향 점수가 아닙니다.
- 플래그는 `흑백만화비중높음`(low_ratio ≥ 0.5), `표본부족`(posts < 30)만 사용합니다.
- 미확인 값은 사분위수에서 제외하고 보고서에 유효 작가 수를 명시합니다.
- `score_norm`은 전체 비삭제 게시물의 연도별 중앙값 기준입니다. 원본 시간대의 연도를 사용하며, 0 분모 또는 posts=0은 `미확인`입니다.
- 다운로드 실패 시 스크립트는 오류를 내고 멈춥니다. 확인하지 못한 수치를 추정해 출력하지 않습니다.
- 실행 완료 시 마지막 줄에 처리 건수와 주요 검증 결과가 JSON으로 출력됩니다.

## 사용자 데이터 결합과 대조

- 기본 입력은 `experiments/EXP-02_StyleLab/pool1_user.txt`와 `artist_ranks_200.csv`입니다. 저장소에 포함된 파일을 사용합니다.
- `--pool-file 경로`, `--ranks-file 경로`로 다른 입력을 지정할 수 있습니다. 파일별 SHA-256과 읽은 내용을 새 실행의 체크포인트에 보존합니다. `--resume`은 저장된 입력을 사용하며, 현재 파일로 조용히 바꾸지 않습니다. 입력을 변경하려면 새 작업 폴더에서 다시 실행합니다.
- pool은 쉼표로 이름을 나누고 공백을 `_`로 바꿔 완전 일치로 결합합니다. 별칭은 추정하지 않습니다. `pool1_포함`은 1/0입니다.
- `평균_순위`·`상위40_등장`은 CSV 원래 값을 결합합니다. 없는 작가는 빈칸, 실제 0회는 0입니다.
- 상관은 지표와 평균 순위가 모두 있는 작가의 Spearman rho입니다. 동률은 평균 순위, 작가별 동일 가중치입니다. n은 작가 수입니다. 평균 순위가 낮을수록 좋으므로 양의 상관은 높은 지표가 나쁜 순위와 연결되는 방향입니다.
- 상관을 새 점수·추천 플래그로 사용하지 않습니다. 한 시드와 혼합 조합에서 얻은 관측이며 독립적인 선호도 검증으로 볼 수 없습니다.

## 검증

`test_artist_metrics.py`는 삭제 제외, 중복/복수 작가, 후보 밖 게시물의 연도 분모 반영, 정확한 태그 일치, OR 중복 방지·realistic 제외, 짝수/음수 점수 중앙값, 연도 경계, 0 분모, posts=0, 사분위수 보간, Spearman의 동률·결측·상수값·방향, 플래그 경계, pool 정규화·중복 키·순위 결합 입력을 수작업 기대값과 비교합니다.
실제 집계에서는 원본 크기·SHA-256, 파일별 Parquet 행 수, 전체 행 수 분해, 작가별 점수·연도·등급 빈도 합을 추가 검증합니다.
