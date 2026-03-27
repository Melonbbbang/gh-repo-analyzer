import os
import time
import requests
from google import genai  # 최신 google-genai 라이브러리 사용
from dotenv import load_dotenv

load_dotenv()

# 1. 제미나이 클라이언트 설정
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def get_all_files_recursive(owner, repo, path="", token=None):
    """폴더 안의 폴더까지 모든 파일을 찾아내는 재귀 함수"""
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    headers = {"Authorization": f"token {token}"} if token else {}
    response = requests.get(url, headers=headers)
    
    exclude_dirs = ['test', 'docs', 'node_modules', 'venv', 'dist', 'build'] # 제외할 폴더들

    files = []
    if response.status_code == 200:
        items = response.json()
        for item in items:
            # 1. 제외 폴더인지 확인
            if any(ex in item['path'].lower() for ex in exclude_dirs):
                continue
                
            if item['type'] == 'dir':
                files.extend(get_all_files_recursive(owner, repo, item['path'], token))
            elif item['type'] == 'file':
                # 2. 핵심 확장자만 남기기 (필요한 것만 골라 쓰세요!)
                if item['name'].endswith(('.py', '.js', '.ts', '.go', '.cpp')):
                    files.append(item)
    return files

def analyze_code_deeply(file_path, code_text):
    """Gemini 3 Flash-Preview를 사용한 코드 정밀 해부"""
    prompt = f"""
    당신은 코드 리버스 엔지니어링 전문가입니다. 다음 파일을 분석하세요: [{file_path}]
    
    1. 파일 역할: 이 파일이 전체 시스템에서 하는 일은 무엇인가요?
    2. 핵심 로직: 이 파일에서 가장 중요한 함수나 알고리즘 2~3가지를 설명해 주세요.
    3. 연결성: 이 파일이 의존하고 있는 다른 파일이나 라이브러리는 무엇인가요?
    4. 코드 학습 포인트: 이 코드에서 배울만한 디자인 패턴이나 효율적인 코딩 방식이 있나요?
    5. 중요도 점수: 1~10점 사이로 평가하고 그 이유를 짧게 적어주세요.
    
    [코드 내용]
    {code_text}
    """
    
    # 최신 SDK 호출 방식 (Gemini 3 Flash Preview 모델 사용)
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )
    
    return response.text

def save_analysis(repo_name, file_path, analysis_text):
    """내 컴퓨터에 깃허브와 똑같은 폴더 구조로 분석 결과 저장"""
    
    # 2. 저장 경로 설정 (경로 오류 방지를 위해 r을 붙인 Raw String 사용)
    # USER 부분은 본인의 PC 사용자 이름에 맞게 확인해 주세요.
    target_folder = "C:/Users/USER/OneDrive/Desktop/Project B 예시/analysis_results/" # Enter your folder address where you want to save the folders
    base_dir = os.path.join(target_folder, repo_name)
    
    # 3. 파일이 들어갈 실제 하위 폴더 경로 생성
    full_local_dir = os.path.join(base_dir, os.path.dirname(file_path))
    
    # 4. 폴더가 없으면 자동으로 생성 (중간 경로까지 모두 생성)
    if not os.path.exists(full_local_dir):
        os.makedirs(full_local_dir)
        
    # 5. 분석 결과 저장 (파일명 뒤에 _analysis.txt를 붙임)
    file_name = os.path.basename(file_path) + "_analysis.txt"
    final_path = os.path.join(full_local_dir, file_name)
    
    with open(final_path, "w", encoding="utf-8") as f:
        f.write(analysis_text)
    
    print(f"✅ 저장 완료: {final_path}")
    return base_dir


def generate_final_summary(repo_name, all_analyses):
    """모든 파일의 분석 결과를 합쳐서 최종 가이드라인 생성"""
    
    combined_context = "\n\n".join(all_analyses)
    
    prompt = f"""
    당신은 이 프로젝트의 리드 개발자입니다. 다음 분석 데이터를 바탕으로 
    전체적인 프로그램 목적과 사용법을 요약한 [Final_Project_Guide.txt] 내용을 작성하세요.
    
    [분석 데이터]
    {combined_context[:10000]}
    """

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )
    
    # 1. 저장 경로 설정
    target_folder = r"C:/Users/USER/OneDrive/Desktop/Project B 예시/analysis_results"
    repo_dir = os.path.join(target_folder, repo_name)
    
    # ⭐ 2. [추가] 폴더가 없으면 생성 (이 부분이 빠져서 오류가 났던 겁니다!)
    if not os.path.exists(repo_dir):
        os.makedirs(repo_dir)
    
    final_path = os.path.join(repo_dir, "Final_Project_Guide.txt")
    
    # 3. 이제 안전하게 저장
    with open(final_path, "w", encoding="utf-8") as f:
        f.write(response.text)
    
    return final_path