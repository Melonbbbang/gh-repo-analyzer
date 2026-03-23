# main.py
import os
import requests
from google import genai
from dotenv import load_dotenv

load_dotenv()

# 공통 클라이언트 설정
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def parse_github_url(url):
    clean_url = url.replace("https://", "").replace("http://", "").strip()
    parts = clean_url.split('/')
    if len(parts) >= 3 and "github.com" in parts[0]:
        return parts[1], parts[2]
    return None, None

def get_repo_content(owner, repo):
    github_token = os.getenv("GITHUB_TOKEN")
    url = f"https://api.github.com/repos/{owner}/{repo}/contents"
    headers = {"Authorization": f"token {github_token}"} if github_token else {}
    
    response = requests.get(url, headers=headers)    
    if response.status_code == 200:
        items = response.json()
        all_code = "" 
        for item in items:
            if item['type'] == 'file' and item['name'].endswith(('.py', '.md')):
                content = requests.get(item['download_url']).text
                all_code += f"\n[File: {item['name']}]\n{content[:5000]}\n"
        return all_code
    return None

def analyze_with_gemini(code_text):
    prompt = f"당신은 IT 창업가입니다. 다음 코드를 분석해줘:\n\n{code_text}"
    response = client.models.generate_content(
        model="gemini-3-flash-preview", 
        contents=prompt
    )
    return response.text