# app.py
import streamlit as st
import main  # 👈 핵심: main.py 파일을 통째로 불러옵니다!

st.set_page_config(page_title="GH-Analyzer", layout="centered")

st.title("🚀 GitHub Repo AI Analyzer")
target_url = st.text_input("GitHub URL 입력")

if st.button("분석 시작 ✨"):
    if target_url:
        # main.py에 있는 함수들을 main.함수명() 형태로 사용합니다.
        owner, repo = main.parse_github_url(target_url)
        
        if owner and repo:
            with st.spinner("분석 중..."):
                context = main.get_repo_content(owner, repo)
                if context:
                    report = main.analyze_with_gemini(context)
                    st.success("✅ 분석 완료!")
                    st.info(report)
                else:
                    st.error("데이터 수집 실패")
        else:
            st.warning("URL 형식을 확인하세요.")