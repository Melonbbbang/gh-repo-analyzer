# 🚀 Project B: Code Sniper (Repo Deep Analyzer)

> **"숲을 보고 나무를 분석한다."** > GitHub 레포지토리의 전체 구조를 내 컴퓨터로 복제하고, Gemini 3 Flash AI를 이용해 파일 하나하나의 핵심 로직과 연결성을 정밀 분석하는 도구입니다.

---

## 🌟 주요 기능 (Core Features)

1.  **Recursive Repo Traversal**: 깃허브 API를 활용해 폴더 안의 폴더까지 모든 파일을 샅샅이 찾아냅니다. (`main.py` 재귀 함수 구현)
2.  **AI-Powered Code Analysis**: 최신 `Gemini 3 Flash-Preview` 모델을 사용하여 코드의 역할, 핵심 로직, 의존성, 학습 포인트를 추출합니다.
3.  **Local Structure Mirroring**: 분석 결과를 깃허브의 원본 폴더 구조와 똑같이 내 로컬 컴퓨터(`Project B 예시` 폴더)에 자동 생성합니다.
4.  **Real-time UI**: `Streamlit`을 통해 분석 진행 상황(Progress Bar)을 실시간으로 확인하고 제어할 수 있습니다.
5.  **API Rate Limiting**: 무료 API 사용량을 고려하여 `time` 라이브러리로 속도를 조절, 안정적인 대량 분석을 지원합니다.

---

## 🛠️ 사용된 기술 스택 (Tech Stack)

| 구분 | 기술 / 라이브러리 |
| :--- | :--- |
| **Language** | Python 3.11+ |
| **Frontend** | Streamlit |
| **AI Model** | Google Gemini 3 Flash Preview |
| **Libraries** | `google-genai`, `requests`, `python-dotenv`, `os`, `time` |

---

## 📂 프로젝트 구조 (Architecture)

- `app.py`: 사용자가 URL을 입력하고 분석 과정을 모니터링하는 웹 인터페이스(조종석).
- `main.py`: 파일 수집, AI 분석 호출, 로컬 파일 저장 로직이 담긴 엔진(본체).
- `.env`: API 키와 같은 민감한 정보를 안전하게 관리하는 설정 파일.
- `analysis_results/`: 분석 완료된 리포트가 깃허브 구조 그대로 저장되는 결과 저장소.

---

## ⚙️ 설치 및 실행 방법 (How to Run)

1. **가상환경 설정 및 필수 라이브러리 설치**
   ```bash
   pip install streamlit requests google-genai python-dotenv


2. **환경 변수 설정**
.env 파일에 GOOGLE_API_KEY=~~

3. **프로그램 실행**
streamlit run app.py