# Meeting Intelligence Agent

[![Python CI](https://github.com/Samadritaacharya/meeting-intelligence-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/Samadritaacharya/meeting-intelligence-agent/actions/workflows/ci.yml)

**A meeting-to-workflow automation system that converts transcripts into structured summaries, decisions, actions, risks, open questions, follow-up communication, and exportable project artifacts.**

[**Open live app →**](https://meeting-intelligence-agent.streamlit.app/) · [Source](https://github.com/Samadritaacharya/meeting-intelligence-agent)

> The public demo works without model credentials through a deterministic fallback analyzer. Sample data is synthetic; no confidential employer, client, or personal data is included.

## What it produces

- leadership-ready executive summary
- key decisions with context
- action-item table with owner, deadline, priority, and status
- risk register with impact, likelihood, mitigation, and owner
- open questions and clarification needs
- project status card with RAG status and escalation needs
- professional follow-up email draft
- downloadable PDF and DOCX reports
- Jira-ready action-item CSV
- risk-register CSV
- Markdown notes for Notion, Confluence, or GitHub

## Operating modes

### Zero-key public mode

The deployed application works without secrets through a deterministic fallback analyzer, keeping the end-to-end workflow available even when no external AI API is configured.

### Optional Anthropic mode

Set these variables locally or in Streamlit Secrets:

```text
ANTHROPIC_API_KEY=<your key>
ANTHROPIC_MODEL=<a model ID available to your account>
```

If the key, model, quota, or API is unavailable, the application falls back safely instead of breaking.

### Optional local audio mode

Audio transcription requires `openai-whisper` and FFmpeg. It is a local optional capability and is not required by the public deployment.

## Architecture

```text
app.py
├── Streamlit interface and session state
├── meeting-type templates
├── structured project result views
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
├── action CSV
├── risk CSV
└── Markdown export
```

## Verification

The repository includes automated fallback/configuration/validation tests, Python compile checks, and GitHub Actions. The public workflow is intentionally usable without a paid API dependency.

## Technology

`Python 3.11` · `Streamlit` · `Pandas` · `Anthropic SDK` · `python-docx` · `fpdf2` · `pytest` · `GitHub Actions`

## Run locally

```bash
git clone https://github.com/Samadritaacharya/meeting-intelligence-agent.git
cd meeting-intelligence-agent
python -m venv .venv
```

```bash
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate
```

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pytest -q
python -m streamlit run app.py
```

## Design principle

A useful meeting assistant should not stop at summarization. It should turn discussion into **decisions, owners, deadlines, risks, follow-up, and reusable operational artifacts**.
