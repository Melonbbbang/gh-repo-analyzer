# 🚀 GH-REPO-Analyzer: AI-Powered GitHub Repository

**GH-Analyzer** is a specialized tool designed to bridge the gap between technical codebases and business strategy. By leveraging the cutting-edge **Gemini 3 Flash Preview** model, it automatically crawls GitHub repositories and generates concise business value reports.

---

## ✨ Key Features
* **Automated Code Extraction:** Fetches source code and documentation directly from GitHub via the GitHub API.
* **AI-Driven Analysis:** Utilizes Google's latest **Gemini 3 Flash Preview** to summarize project functionality and market potential.
* **Seamless URL Parsing:** Simply input a GitHub URL, and the tool intelligently extracts the owner and repository information.
* **Modern Web Interface:** Built with **Streamlit** for a clean, fast, and responsive user experience.

---

## 🛠️ Tech Stack
* **Language:** Python 3.11+
* **AI Engine:** Google Generative AI (Gemini 3 Flash Preview)
* **Web Framework:** Streamlit
* **Data Sourcing:** GitHub REST API

---

## ⚙️ Getting Started

### 1. Prerequisites
Ensure you have a Google AI Studio API Key and a GitHub Personal Access Token (optional but recommended for rate limits).

### 2. Installation
```bash
# Clone the repository
git clone [https://github.com/Melonbbbang/gh-repo-analyzer.git](https://github.com/Melonbbbang/gh-repo-analyzer.git)
cd gh-repo-analyzer

# Setup virtual environment
python -m venv venv
source venv/Scripts/activate  # On Windows

# Install dependencies
pip install -r requirements.txt

### 3. Environment Variables
# .env file content
GOOGLE_API_KEY=your_google_api_key_here
GITHUB_TOKEN=your_github_token_here

### 4. Run the Application
# Ensure your venv is activated before running
streamlit run app.py