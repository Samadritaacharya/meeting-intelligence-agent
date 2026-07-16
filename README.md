# Meeting Intelligence Agent

A recruiter-demo-ready PMO workflow assistant that converts meeting transcripts into structured executive summaries, decisions, action items, risks, open questions, follow-up emails, and exportable reports.

[![Python CI](https://github.com/Samadritaacharya/meeting-intelligence-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/Samadritaacharya/meeting-intelligence-agent/actions/workflows/ci.yml)

**Live application:** [meeting-intelligence-agent.streamlit.app](https://meeting-intelligence-agent.streamlit.app/)  
**Portfolio owner:** [Samadrita Acharya](https://www.linkedin.com/in/samadrita-acharya-a07266184/)

## Recruiter quick view

| Area | Evidence in this project |
|---|---|
| Business problem | Unstructured meetings create unclear decisions, ownership, deadlines, risks, and follow-up communication. |
| Product solution | A Streamlit workflow that converts a transcript into PMO-ready outputs and downloadable reports. |
| Technical implementation | Python, Streamlit, Pandas, Anthropic-compatible API integration, deterministic fallback analysis, PDF/DOCX/CSV/Markdown export. |
| Delivery thinking | Meeting templates, RAG status, action ownership, risk mitigation, escalation needs, and Jira-ready exports. |
| Reliability | Safe demo mode without an API key, explicit model configuration, graceful API-error fallback, automated tests, and GitHub Actions. |
| Data/privacy | Uses user-provided or synthetic sample text; no confidential employer or client data is included. |

## What the application produces

- leadership-ready executive summary
- key decisions with context
- action-item table with owner, deadline, priority, and status
- risk register with impact, likelihood, mitigation, and owner
- open questions and clarification needs
- PMO status card with RAG status and decision/escalation needs
- professional follow-up email draft
- downloadable PDF and DOCX reports
- Jira-ready action-item CSV
- risk-register CSV
- Markdown notes for Notion, Confluence, or GitHub

## Two-minute recruiter demo

1. Open the [live app](https://meeting-intelligence-agent.streamlit.app/).
2. Select a meeting type such as **Steering committee** or **Incident review**.
3. Choose **Load sample** and click **Load and analyze sample**.
4. Review the executive summary, RAG status, decisions, actions, and risks.
5. Download a PDF, DOCX, Jira CSV, risk CSV, or Markdown report.
6. Explain how the workflow supports PMO governance, technical project coordination, cloud operations, ITSM, or product operations.

## Operating modes

### Public portfolio mode

The deployed application works without secrets through a deterministic fallback analyzer. This keeps the complete sample workflow available to recruiters and reviewers even when no external AI API is configured.

### Live Claude mode

Set both variables below locally or in Streamlit Secrets:

```text
ANTHROPIC_API_KEY=<your key>
ANTHROPIC_MODEL=<a model ID available to your Anthropic account>
```

The model ID is deliberately configuration-driven rather than hard-coded. If the key, model, quota, or API is unavailable, the application returns to demo mode instead of breaking.

### Optional local audio mode

Audio transcription requires `openai-whisper` and FFmpeg. It is an optional local capability and is **not presented as guaranteed functionality on the public Streamlit deployment**.

## Architecture

```text
app.py
├── Streamlit interface and session state
├── meeting-type templates
├── structured PMO result views
└── report download controls

utils/analyzer.py
├── Anthropic API workflow
├── deterministic no-key fallback
├── response normalization
├── API/model error handling
└── optional local Whisper transcription

utils/exporter.py
├── PDF export
├── DOCX export
├── Jira action CSV
├── risk CSV
└── Markdown export

sample_data/sample_transcript.txt
└── synthetic recruiter-demo transcript

tests/test_analyzer.py
└── fallback, configuration, validation, and JSON parsing tests
```

## Technology stack

| Layer | Technology |
|---|---|
| Interface | Streamlit |
| Language | Python 3.11 |
| AI integration | Anthropic Python SDK with configurable model ID |
| Demo continuity | Deterministic rule-based fallback analyzer |
| Data presentation | Pandas |
| Documents | python-docx, fpdf2, CSV, Markdown |
| Quality | pytest, Python compile checks, GitHub Actions |
| Deployment | Streamlit Community Cloud; Docker-compatible repository |

## Run locally

```bash
git clone https://github.com/Samadritaacharya/meeting-intelligence-agent.git
cd meeting-intelligence-agent
python -m venv .venv
```

Activate the environment:

```bash
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate
```

Install, test, and run:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pytest -q
python -m streamlit run app.py
```

## Why this project matters for my target roles

This project connects AI workflow design with the execution disciplines required in technical project management: converting discussion into decisions, owners, deadlines, risks, governance signals, and reusable stakeholder communication.

It is especially relevant to roles in:

- Technical Project Management and PMO
- AI Transformation and workflow automation
- Cloud Delivery and AIOps coordination
- ITSM / incident-review operations
- Product and business operations
- Digital Transformation

## CV / LinkedIn project description

> Built a Python and Streamlit Meeting Intelligence Agent that converts meeting transcripts into executive summaries, decision logs, action-item tables, risk registers, RAG status, follow-up emails, and downloadable PDF/DOCX/CSV/Markdown reports. Added deterministic demo continuity, configurable Anthropic integration, automated tests, and GitHub Actions.

## Responsible portfolio use

This is an independent portfolio project. It is not affiliated with SAP, IBM, Kyndryl, RWTH Aachen University, Anthropic, or any client organization. The repository contains no confidential employer, university, customer, or personal data.
