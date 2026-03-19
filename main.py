import os
import requests
from dotenv import load_dotenv

# 1. .env 파일에 저장된 비밀번호들 불러오기
load_dotenv()
github_token = os.getenv("GITHUB_TOKEN")

def get_repo_files(repo_owner, repo_name):
    """지정한 깃허브 레포지토리의 파일 목록을 가져오는 함수"""
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents"
    # 토큰이 있으면 헤더에 추가하고, 없으면 빈 상태로 보냅니다.
    headers = {"Authorization": f"token {github_token}"} if github_token else {}
    
    response = requests.get(url, headers=headers)
    
    # [수정된 부분] status_status -> status_code
    if response.status_code == 200:
        files = response.json()
        print(f"\n--- [{repo_name}] 파일 목록 ---")
        for file in files:
            print(f"파일명: {file['name']} ({file['type']})")
    else:
        print(f"오류 발생: {response.status_code}")
        print(f"메시지: {response.json().get('message')}")

# 테스트 실행
if __name__ == "__main__":
    # 구글의 공개 저장소로 테스트해봅니다.
    get_repo_files("google", "googletest")