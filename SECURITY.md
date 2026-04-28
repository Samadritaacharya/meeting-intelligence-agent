# Security Notes

## Secrets

- Do **not** commit `.env` or `.streamlit/secrets.toml`.
- Store `ANTHROPIC_API_KEY` in local `.env` for development.
- Store `ANTHROPIC_API_KEY` in Streamlit Cloud **Secrets** for deployment.
- The repository includes `.env.example` and `.streamlit/secrets.toml.example` only as templates.

## Data Privacy

- Transcript text is sent to Anthropic only when a valid `ANTHROPIC_API_KEY` is configured.
- Audio transcription is optional and runs locally when `openai-whisper` and `ffmpeg` are installed.
- Uploaded audio is written to a temporary file and deleted after processing.
- Exported reports are generated in memory and offered as downloads.

## Input/Output Safety

- User and model-generated text is escaped before being rendered inside custom HTML containers.
- The app uses a deterministic fallback mode when no API key is configured so the UI remains demoable without exposing secrets.

## Recommended Production Settings

- Use Streamlit Cloud secrets or environment variables; never hardcode keys.
- Rotate API keys if they are accidentally shared.
- Review model outputs before sending generated follow-up emails externally.
- Avoid uploading confidential meeting content to public demo deployments unless your API/data policy allows it.
