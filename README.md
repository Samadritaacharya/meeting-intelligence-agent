# 🎙️ Meeting Intelligence Agent

> Premium AI-powered meeting analysis app that turns transcripts into executive summaries, decisions, risks, action items, and ready-to-send follow-up emails.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-ff4b4b)
![Claude](https://img.shields.io/badge/Claude-API-orange)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ What this project does

Meeting Intelligence Agent helps product, project, operations, and leadership teams convert messy meeting transcripts into structured, actionable outputs.

The app can generate:

- 📌 Executive summaries
- ✅ Action items
- 🧠 Key decisions
- ⚠️ Risks and blockers
- ❓ Open questions
- 📧 Follow-up email drafts
- 📄 Export-ready PDF and Word documents

It is designed as a portfolio-quality AI product demonstrating practical LLM integration, structured prompting, UX thinking, security awareness, and deployment readiness.

## 🧩 Product narrative

Most meetings create unstructured notes, unclear ownership, and follow-up gaps. This project solves that workflow with a simple AI-first interface:

1. Paste a transcript or load the sample meeting.
2. Claude analyzes the meeting using a structured JSON prompt.
3. The UI renders PM-ready outputs in a premium orange/dark interface.
4. Users can export the results or copy the follow-up email.

## 🛠️ Tech stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| AI Engine | Anthropic Claude API |
| Language | Python |
| Config | python-dotenv + Streamlit Secrets |
| Export | python-docx + fpdf2 |
| Deployment | Streamlit Cloud / Docker |
| CI | GitHub Actions |

## 🔐 Security-first design

This repository is safe for public GitHub usage:

- No API keys are committed.
- `.env` and Streamlit secrets are ignored.
- `.env.example` is provided for local setup.
- User and AI-generated text is escaped before being rendered inside custom HTML cards.
- Claude receives only the submitted transcript text and optional metadata.
- A fallback demo mode works without an API key for portfolio review.

See [SECURITY.md](SECURITY.md) for details.

## 🚀 Quick start locally

```bash
git clone https://github.com/Samadritaacharya/meeting-intelligence-agent.git
cd meeting-intelligence-agent
python -m venv venv
```

### Windows PowerShell

```powershell
venv\Scripts\activate
```

### macOS / Linux

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Create local environment file:

```bash
cp .env.example .env
```

On Windows, you can also create it manually:

```powershell
copy .env.example .env
notepad .env
```

Add your Anthropic API key:

```env
ANTHROPIC_API_KEY=sk-ant-your-real-key-here
```

Run the app:

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

## 🌐 Deploy on Streamlit Cloud

1. Go to <https://share.streamlit.io/>
2. Create a new app.
3. Select this repository.
4. Use:

```text
Branch: main
Main file path: app.py
```

5. Add this in Streamlit Cloud secrets:

```toml
ANTHROPIC_API_KEY = "sk-ant-your-real-key-here"
```

6. Deploy and share the public URL.

## 🧪 Demo mode

The app includes a sample transcript and can run without an API key using deterministic fallback analysis. This makes the project reviewable even before configuring secrets.

## 📂 Repository structure

```text
meeting-intelligence-agent/
├── app.py
├── requirements.txt
├── README.md
├── SECURITY.md
├── DEPLOYMENT.md
├── Dockerfile
├── .env.example
├── .gitignore
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml.example
├── sample_data/
│   └── sample_transcript.txt
└── utils/
    ├── __init__.py
    ├── analyzer.py
    └── exporter.py
```

## 🎯 Why this is portfolio-relevant

This project demonstrates skills that are highly relevant for AI product, AI operations, and technical project management roles:

- Building usable AI workflows instead of notebooks only
- Translating a business pain point into a working product
- Structured LLM prompting and JSON output handling
- Secure secret management and deployment readiness
- UX-focused product packaging
- Documentation quality for open-source users

## 🗺️ Roadmap

- [ ] Add audio upload with local Whisper transcription
- [ ] Add meeting templates by use case: sprint planning, stakeholder review, incident review
- [ ] Add priority scoring for action items
- [ ] Add Notion/Jira export integration
- [ ] Add multi-model comparison mode

## 📄 License

MIT License. See [LICENSE](LICENSE).

---

Built as an AI portfolio project by **Samadrita Acharya**.
