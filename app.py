import streamlit as st
import main # 위에서 만든 main.py 불러오기
import time
import requests

st.title("🚀 Code Sniper: Repo Deep Analyzer")
repo_url = st.text_input("분석할 GitHub Repository URL을 입력하세요")

if st.button("코드 정밀 해부 시작"):
    if repo_url:
        # URL에서 owner와 repo 추출 (기존 로직 활용)
        owner, repo = repo_url.split('/')[-2], repo_url.split('/')[-1]
        
        with st.spinner("📦 파일 목록 불러오는 중..."):
            all_files = main.get_all_files_recursive(owner, repo)
        
        st.write(f"📂 총 {len(all_files)}개의 파일을 발견했습니다.")
        
        # 진행바 생성
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for idx, file_item in enumerate(all_files):
            file_path = file_item['path']
            status_text.text(f"🧠 {file_path} 분석 중... (무료 API 속도 조절 중)")
            
            # 코드 가져오기
            code_content = requests.get(file_item['download_url']).text
            
            # 분석 및 저장
            analysis = main.analyze_code_deeply(file_path, code_content)
            main.save_analysis(repo, file_path, analysis)
            
            # 진행도 업데이트
            progress_bar.progress((idx + 1) / len(all_files))
            
            # ⭐ 무료 버전 API 제한(RPM)을 피하기 위해 4초 대기
            time.sleep(4)

            final_path = main.save_analysis(repo, file_path, analysis)
            
        st.success(f"✅ 분석 완료! 저장 폴더 : {final_path}")