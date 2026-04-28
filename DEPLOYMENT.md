# Deployment Guide

## Local Run

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

Open `http://localhost:8501`.

## Streamlit Cloud

1. Push this repository to GitHub.
2. Open https://share.streamlit.io/.
3. Select the repository.
4. Set main file path to `app.py`.
5. Add this in **Settings > Secrets**:

```toml
ANTHROPIC_API_KEY = "sk-ant-your-real-key-here"
```

6. Redeploy and test the **Load sample** tab first.

## Docker

```bash
docker build -t meeting-intelligence-agent .
docker run -p 8501:8501 -e ANTHROPIC_API_KEY="sk-ant-your-real-key-here" meeting-intelligence-agent
```

## Optional Audio Transcription

Audio support requires Whisper and ffmpeg. Install manually when needed:

```bash
pip install openai-whisper
```

Then install ffmpeg using your system package manager.
