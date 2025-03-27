# 🧠 Multi AI Agent System for Banking

A collaborative AI-driven app that writes news-style financial reports on the world's top banks — in real time.  
Each agent does one job: searching, analyzing, fact-checking, writing. Together, they act like a newsroom… but smarter.

> Built with 💬 OpenAI, 🕵️ Tavily, 🧱 CrewAI and ⚡ Dash.

---

## ✨ Features

- 🧑‍💼 Multiple autonomous agents working together
- 🔎 Real-time data collection via Tavily Search API
- ✍️ GPT-generated banking news reports
- 📊 Clean, interactive Dash web interface
- 🔁 Modular prompt-based architecture with CrewAI

---

## 📸 Preview

![screenshot-placeholder](https://via.placeholder.com/800x400.png?text=Screenshot+coming+soon)

---

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/banking-ai-system.git
cd banking-ai-system

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

⚠️ **Don’t forget to add your API keys to the .env file:**

- OPENAI_API_KEY
- TAVILY_API_KEY

## 🧠 How It Works

1. **User selects a bank**
2. **Agents are launched via CrewAI:**
   - `ResearchAgent` — finds relevant sources  
   - `AnalysisAgent` — extracts insights  
   - `WriterAgent` — composes the report  
   - `FactCheckerAgent` — ensures accuracy
3. **Dash frontend** renders the final report with interactive visuals

---

## 🔧 Skills & Tools Used

`Python` &nbsp; `Dash` &nbsp; `Plotly` &nbsp; `CrewAI` &nbsp; `LangChain` &nbsp; `OpenAI API` &nbsp; `Tavily Search` &nbsp; `Prompt Engineering` &nbsp; `LLM Collaboration`

---

This project is a portfolio experiment in multi-agent orchestration with real-world applications in business intelligence, financial journalism, and automated reporting.

It was developed as part of a community project within [Charming Data](https://charming-data.circle.so/c/ai-python-projects/) — a space for building open-source AI & Python applications together.

---

## 💬 Fun Fact

The most satisfying part? Watching one AI agent ask another:  
**"Can you double-check the numbers in the source?"**

---

## 📄 License

MIT © 2025 [Alexandra Meshi](https://github.com/svechino)
