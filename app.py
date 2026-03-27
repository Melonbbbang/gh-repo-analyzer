import streamlit as st
import main # 위에서 만든 main.py 불러오기
import time
import requests
import os

st.title("🚀 Code Sniper: Repo Deep Analyzer")
repo_url = st.text_input("분석할 GitHub Repository URL을 입력하세요")

if st.button("코드 정밀 해부 시작"):
    if repo_url:
        # URL에서 owner와 repo 추출
        owner, repo = repo_url.split('/')[-2], repo_url.split('/')[-1]
        
        with st.spinner("📦 파일 목록 불러오는 중..."):
            all_files = main.get_all_files_recursive(owner, repo)
        
        st.write(f"📂 총 {len(all_files)}개의 파일을 발견했습니다.")
        
        # ⭐ [추가] 모든 분석 결과를 담을 리스트
        all_analyses = []
        
        # 진행바 생성
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for idx, file_item in enumerate(all_files):
            file_path = file_item['path']

            # --- [추가] 이어하기 체크 로직 ---
            # 저장될 파일의 전체 경로를 미리 계산해봅니다.
            target_folder = r"C:/Users/USER/OneDrive/Desktop/Project B 예시/analysis_results"
            file_name = os.path.basename(file_path) + "_analysis.txt"
            full_local_path = os.path.join(target_folder, repo, os.path.dirname(file_path), file_name)
    
            if os.path.exists(full_local_path):
             status_text.text(f"⏩ {file_path} (이미 분석됨, 건너뜁니다)")
             # 이미 파일이 있다면 분석 단계를 통째로 점프!
             progress_bar.progress((idx + 1) / len(all_files))
             continue 
    # -------------------------------


            
            status_text.text(f"🧠 {file_path} 분석 중... ({idx+1}/{len(all_files)})")
            
            # 코드 가져오기
            code_content = requests.get(file_item['download_url']).text
            
            # 분석 및 저장
            analysis = main.analyze_code_deeply(file_path, code_content)
            main.save_analysis(repo, file_path, analysis)
            
            # ⭐ [추가] 나중에 종합 요약을 만들기 위해 리스트에 저장
            all_analyses.append(f"--- 파일: {file_path} ---\n{analysis}")
            
            # 진행도 업데이트
            progress_bar.progress((idx + 1) / len(all_files))
            
            # 무료 버전 API 제한(RPM)을 피하기 위해 대기
            time.sleep(4)

        # ⭐ [추가] 모든 파일 분석이 끝난 후 최종 요약 가이드 생성
        status_text.text("📝 모든 파일을 읽었습니다. 전체 프로젝트 가이드를 작성 중입니다...")
        final_guide_path = main.generate_final_summary(repo, all_analyses)
        
        # 최종 성공 메시지 (최종 가이드 경로 출력)
        st.success(f"✅ 모든 분석 완료! 프로젝트 가이드는 아래 경로에서 확인하세요.")
        st.info(f"📁 가이드 파일: {final_guide_path}")