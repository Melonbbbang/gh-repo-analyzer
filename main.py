import os
import requests
from google import genai 
from dotenv import load_dotenv

load_dotenv()
github_token = os.getenv("GITHUB_TOKEN")
google_api_key = os.getenv("GOOGLE_API_KEY")

# 1. 클라이언트 생성 (가장 기본형으로 되돌립니다)
# http_options를 넣었을 때 404가 난다면, 라이브러리 자동 감지에 맡기는 게 최선입니다.
client = genai.Client(api_key=google_api_key)

def get_repo_content(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents"
    headers = {"Authorization": f"token {github_token}"} if github_token else {}
    
    response = requests.get(url, headers=headers)    
    if response.status_code == 200:
        items = response.json()
        all_code = "" 
        for item in items:
            if item['type'] == 'file' and item['name'].endswith(('.py','.md')):
                content = requests.get(item['download_url']).text
                all_code += f"\n[File: {item['name']}]\n{content[:10000]}\n"
        return all_code
    return None

def analyze_with_gemini(code_text):
    prompt = f"당신은 IT 창업가입니다. 다음 코드를 요약해줘: \n\n{code_text}"
    
    try:
        # 핵심 수정: 모델 이름 앞에 'models/'를 명시적으로 붙여줍니다.
        # 구글 에러 메시지에 'models/gemini-1.5-flash'를 찾을 수 없다고 했으므로, 
        # 이번에는 'gemini-1.5-flash' (경로 없음)로 시도합니다.
        response = client.models.generate_content(
            model="gemini-3-flash-preview", 
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"AI 분석 실패: {e}"

if __name__ == "__main__":
    owner = "Melonbbbang"
    repo = "gh-repo-analyzer"

    context = get_repo_content(owner, repo)
    if context:
        print("🤖 분석 중...")
        report = analyze_with_gemini(context)
        print(report)