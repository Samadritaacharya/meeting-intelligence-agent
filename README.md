# Meeting Intelligence Agent

AI-powered PMO workflow assistant that turns raw meeting transcripts into executive summaries, decisions, action-item tables, risk registers, open questions, follow-up emails, and export-ready reports.

## Live demo

[Open the Meeting Intelligence Agent](https://meeting-intelligence-agent.streamlit.app/)

## Demo mode

The app can run in portfolio demo mode without external configuration. For a live presentation, use the sample transcript workflow.

## Live demo workflow

1. Open the live app.
2. Select a meeting type / PMO template in the sidebar.
3. Paste a transcript or click **Load and analyze sample**.
4. Click **Analyze transcript** when using your own text.
5. Review the executive summary, decisions, action table, risk register, PMO status and follow-up email.
6. Export PDF, DOCX, Jira CSV, risk CSV or Markdown notes.

## Business problem

Project, product, operations and cloud-delivery meetings often produce unstructured notes. Decisions, owners, risks, deadlines and open questions can become unclear after the meeting, especially in cross-functional environments.

This project solves that workflow problem by converting meeting transcripts into PMO-ready outputs that can be reviewed, exported and reused for follow-ups, Jira imports, risk registers and stakeholder communication.

## Solution

The app provides a simple workflow:

1. Select the meeting type / PMO template.
2. Paste a transcript, upload audio, or load the sample transcript.
3. Analyze the meeting.
4. Review structured outputs: summary, decisions, action table, risks, open questions, PMO status and follow-up email.
5. Export the results to PDF, DOCX, Jira-ready CSV, risk CSV or Markdown notes.

## Key features

- Executive meeting summaries
- Key decision extraction
- Structured action-item table with owner, action, due date, priority and status
- Risk register with impact, likelihood, mitigation and owner
- Open-question extraction
- PMO status card with RAG status, health, decision needed and next review
- Meeting templates for Project sync, Steering committee, Incident review, Sprint planning, Vendor discussion and Stakeholder workshop
- Follow-up email draft
- PDF and DOCX report export
- Jira-ready CSV export for action items
- Risk CSV export
- Markdown export for Notion/GitHub notes
- Demo/fallback mode for portfolio review

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| AI workflow | Claude-compatible analysis plus fallback demo mode |
| Language | Python |
| Data display | Pandas |
| Export | python-docx, fpdf2, CSV, Markdown |
| Deployment | Streamlit Cloud / Docker |

## Quick start locally

```bash
git clone https://github.com/Samadritaacharya/meeting-intelligence-agent.git
cd meeting-intelligence-agent
python -m venv venv
pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

## Why this project is relevant to my target roles

This project connects to PMO, technical project coordination, cloud operations and digital transformation roles because meeting outputs must become clear actions, risks, owners and decisions.

Relevant target roles:

- Technical Project Coordinator
- PMO Analyst
- Junior Project Manager
- AI Transformation Associate
- Cloud Operations / AIOps Coordinator
- Product Operations Analyst
- Digital Transformation Associate

## CV bullet

Developed an AI-powered Meeting Intelligence Agent using Python and Streamlit to convert meeting transcripts into executive summaries, decisions, action-item tables, risk registers, open questions and export-ready PDF/DOCX/CSV/Markdown reports.

## Disclaimer

This is an independent portfolio project. No confidential SAP, IBM, Kyndryl, university or client data is used.
