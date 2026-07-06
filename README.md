# 🎙️ Meeting Intelligence Agent

> AI-powered PMO workflow assistant that turns raw meeting transcripts into executive summaries, decisions, action-item tables, risk registers, open questions, follow-up emails, and export-ready reports.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-ff4b4b)
![Claude](https://img.shields.io/badge/Claude-API-orange)
![PMO](https://img.shields.io/badge/PMO-Workflow%20Automation-purple)
![License](https://img.shields.io/badge/License-MIT-green)

## Demo

- **Live app:** Deployment-ready; add Streamlit Cloud URL after deployment.
- **Screenshots:** See `assets/screenshots/` after adding exported app screenshots.
- **Demo mode:** Works without an API key through deterministic fallback analysis.

---

## Business problem

Project, product, operations, and cloud-delivery meetings often produce unstructured notes. Decisions, owners, risks, deadlines, and open questions can become unclear after the meeting, especially in cross-functional environments.

This project solves that workflow problem by converting meeting transcripts into PMO-ready outputs that can be reviewed, exported, and reused for follow-ups, Jira imports, risk registers, and stakeholder communication.

---

## Solution

The app provides a simple workflow:

1. Select the meeting type / PMO template.
2. Paste a transcript, upload audio, or load the sample transcript.
3. Analyze the meeting with Claude API or fallback demo mode.
4. Review structured outputs: summary, decisions, action table, risks, open questions, PMO status, and follow-up email.
5. Export the results to PDF, DOCX, Jira-ready CSV, risk CSV, or Markdown/Notion notes.

---

## Key features

- Executive meeting summaries
- Key decision extraction
- Structured action-item table with owner, action, due date, priority, and status
- Risk register with impact, likelihood, mitigation, and owner
- Open-question extraction
- PMO status card with RAG status, health, decision needed, and next review
- Meeting templates for:
  - Project sync
  - Steering committee
  - Incident review
  - Sprint planning
  - Vendor discussion
  - Stakeholder workshop
- Follow-up email draft
- PDF and DOCX report export
- Jira-ready CSV export for action items
- Risk CSV export
- Markdown export for Notion/GitHub notes
- Optional local audio transcription with Whisper
- Secure secret handling through `.env` or Streamlit Secrets
- Demo/fallback mode for portfolio review without API keys

---

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| AI Engine | Anthropic Claude API |
| Language | Python |
| Data display | Pandas |
| Config | python-dotenv + Streamlit Secrets |
| Export | python-docx, fpdf2, CSV, Markdown |
| Deployment | Streamlit Cloud / Docker |
| CI | GitHub Actions |

---

## Architecture

```text
meeting-intelligence-agent/
├── app.py                         # Streamlit UI and PMO workflow
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
├── assets/
│   └── screenshots/
├── sample_data/
│   └── sample_transcript.txt
└── utils/
    ├── analyzer.py                # Claude prompt + fallback analysis
    └── exporter.py                # PDF, DOCX, CSV, Markdown exports
```

---

## Quick start locally

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

On Windows, create it manually if needed:

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

---

## Deploy on Streamlit Cloud

1. Go to Streamlit Community Cloud.
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

6. Deploy and add the public URL to this README under **Demo**.

---

## Example use case

A project manager or PMO analyst pastes a steering committee transcript. The app produces a leadership-ready summary, decisions, RAG status, risks, owners, action items, open questions, a follow-up email, and export-ready files for Jira, Notion, or project documentation.

---

## Skills demonstrated

- AI workflow design
- PMO process automation
- Prompt engineering and structured JSON output handling
- Risk and action-item extraction
- Executive communication support
- Jira-ready CSV workflow thinking
- Exportable project documentation
- Secure secrets management
- Streamlit application development
- Recruiter-friendly product packaging

---

## Why this project is relevant to my target roles

This project directly connects to my experience supporting SAP Cloud Delivery Architecture / AIOps PMO activities and my IBM/Kyndryl IT service operations background. In PMO, technical project coordination, cloud operations, and digital transformation roles, meeting outputs must become clear actions, risks, owners, and decisions.

The project demonstrates how I can translate a real project-management pain point into a working AI-enabled workflow tool.

Relevant target roles:

- Technical Project Coordinator
- PMO Analyst
- Junior Project Manager
- AI Transformation Associate
- Cloud Operations / AIOps Coordinator
- Product Operations Analyst
- Digital Transformation Associate

---

## CV bullet

> Developed an AI-powered Meeting Intelligence Agent using Python, Streamlit and Claude API to convert meeting transcripts into executive summaries, decisions, action-item tables, risk registers, open questions and export-ready PDF/DOCX/CSV/Markdown reports.

---

## LinkedIn post idea

> Meetings create value only when decisions, owners, risks and next steps are captured clearly. I built a Meeting Intelligence Agent to turn unstructured meeting transcripts into PMO-ready outputs: summaries, decisions, action tables, risk registers, open questions, follow-up emails and export-ready reports.

---

## Roadmap

- [x] Add meeting-type templates
- [x] Add action-item table
- [x] Add risk register table
- [x] Add Jira-ready CSV export
- [x] Add Markdown / Notion-ready export
- [ ] Add deployed Streamlit demo URL
- [ ] Add screenshots and short demo GIF
- [ ] Add optional Jira/Notion API integration
- [ ] Add multi-model comparison mode

---

## Security and data disclaimer

- No API keys are committed.
- `.env` and Streamlit secrets are ignored.
- `.env.example` is provided for local setup.
- User and AI-generated text is escaped before being rendered inside custom HTML cards.
- This is an independent portfolio project.
- No confidential SAP, IBM, Kyndryl, university, or client data is used.

See [SECURITY.md](SECURITY.md) for details.

---

Built as an AI portfolio project by **Samadrita Acharya**.
