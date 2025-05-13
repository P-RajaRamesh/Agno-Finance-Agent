# 📊 Agno-Finance-Agent
An AI-powered financial analysis tool built with Streamlit, Google Gemini via the AGNO Agent Framework, and Yahoo Finance. This assistant fetches live market data, delivers detailed financial insights, and presents structured reports — perfect for casual investors, financial enthusiasts, or market analysts.

## 🚀 Features
- 🔍 Real-time stock data via Yahoo Finance
- 📊 Comprehensive analysis reports:
  - Market Overview
  - Financial Deep Dive
  - Analyst Recommendations
  - Market Context & Industry Trends
  - Risk Factors and Disclaimers
- 📈 Emoji-enhanced summaries for quick sentiment assessment
- 📄 Formatted markdown reports with tables and bullet points
- 🔐 Google Gemini API Key management with validation and session storage
- 🎨 Streamlit sidebar instructions & examples

## 🛠️ Tech Stack
- Streamlit — for building the interactive web app
- AGNO Agent Framework — for integrating LLM agents
- Google Gemini API — via AGNO
- Yahoo Finance — for financial data
- Python-dotenv — to manage API keys via environment variables

## 📦 Installation
```
git clone https://github.com/yourusername/Agno-Finance-Agent.git
cd Agno-Finance-Agent
pip install -r requirements.txt
```
## 🔐 Environment Setup
Create a ```.env``` file in the root directory and add your Google Gemini API key:
```
GOOGLE_API_KEY=your_gemini_api_key_here
```
Alternatively, you can enter the key via the Streamlit UI on first launch.

## ▶️ Run the App
```
streamlit run AgnoFinanceAgent.py
```
## 📌 Notes
- Data fetched live via Yahoo Finance APIs
- Uses AGNO's YFinanceTools for stock fundamentals, market data, and news
- API key is securely managed via environment variables and Streamlit session state


