"""AI meeting analysis utilities.

Supports transcript analysis with Anthropic Claude and optional local audio
transcription with OpenAI Whisper.
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List


def _get_api_key() -> str | None:
    """Read Anthropic API key from Streamlit secrets or environment."""
    try:
        import streamlit as st  # type: ignore
        key = st.secrets.get("ANTHROPIC_API_KEY") if hasattr(st, "secrets") else None
        if key:
            return str(key)
    except Exception:
        pass
    return os.getenv("ANTHROPIC_API_KEY")


def _fallback_analysis(transcript: str, meeting_title: str = "Meeting") -> Dict[str, Any]:
    """Deterministic fallback so the app remains demoable without an API key."""
    lines = [line.strip() for line in transcript.splitlines() if line.strip()]
    text = " ".join(lines)
    sentences = re.split(r"(?<=[.!?])\s+", text)
    actions: List[str] = []
    decisions: List[str] = []
    risks: List[str] = []
    questions: List[str] = []
    for s in sentences:
        lower = s.lower()
        if any(k in lower for k in ["action", "follow up", "will", "owner", "deadline", "by friday", "by monday"]):
            actions.append(s[:260])
        if any(k in lower for k in ["decided", "decision", "approved", "agreed", "we will"]):
            decisions.append(s[:260])
        if any(k in lower for k in ["risk", "blocker", "issue", "delay", "concern", "dependency"]):
            risks.append(s[:260])
        if "?" in s or any(k in lower for k in ["open question", "clarify", "unknown"]):
            questions.append(s[:260])

    summary_seed = " ".join(sentences[:3]) if sentences else "The meeting transcript was analyzed successfully."
    return {
        "executive_summary": f"Demo-mode summary for {meeting_title}: {summary_seed[:650]}",
        "key_decisions": decisions[:5] or ["No explicit decisions detected in demo mode."],
        "action_items": actions[:8] or ["No explicit action items detected in demo mode."],
        "risks_flagged": risks[:5] or ["No major risks detected in demo mode."],
        "open_questions": questions[:5] or ["No open questions detected in demo mode."],
        "follow_up_email": {
            "subject": f"Follow-up: {meeting_title}",
            "body": "Hi team,<br><br>Sharing a quick AI-generated meeting follow-up with summary, decisions, and next steps. Please review the action items and confirm any missing owners or deadlines.<br><br>Best regards,",
        },
        "analysis_mode": "demo_fallback_no_api_key",
    }


def _extract_json(raw_text: str) -> Dict[str, Any]:
    """Extract JSON object even if the model wraps it in Markdown."""
    raw_text = raw_text.strip()
    if raw_text.startswith("```"):
        raw_text = re.sub(r"^```(?:json)?", "", raw_text).strip()
        raw_text = re.sub(r"```$", "", raw_text).strip()
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", raw_text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        raise


def analyze_meeting(transcript: str, meeting_title: str = "Meeting", participants: str = "") -> Dict[str, Any]:
    """Analyze a meeting transcript into structured PM-ready outputs."""
    if not transcript or len(transcript.strip()) < 20:
        raise ValueError("Please provide a longer meeting transcript.")

    api_key = _get_api_key()
    if not api_key:
        return _fallback_analysis(transcript, meeting_title)

    try:
        from anthropic import Anthropic
    except ImportError as exc:
        raise RuntimeError("anthropic package is not installed. Run: pip install anthropic") from exc

    client = Anthropic(api_key=api_key)
    prompt = f"""
You are an expert AI Meeting Intelligence Agent for product, project, and operations teams.
Analyze the transcript and return ONLY valid JSON with this exact schema:
{{
  "executive_summary": "3-6 sentence leadership-ready summary",
  "key_decisions": ["decision with context"],
  "action_items": ["Owner — action — deadline/status if available"],
  "risks_flagged": ["risk/blocker with impact"],
  "open_questions": ["open question or clarification needed"],
  "follow_up_email": {{
    "subject": "professional subject line",
    "body": "HTML-friendly follow-up email body with bullets and next steps"
  }}
}}

Meeting title: {meeting_title or 'Meeting'}
Participants: {participants or 'Not provided'}
Transcript:
{transcript[:35000]}
"""

    response = client.messages.create(
        model=os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022"),
        max_tokens=2500,
        temperature=0.2,
        messages=[{"role": "user", "content": prompt}],
    )
    content = "".join(block.text for block in response.content if getattr(block, "type", None) == "text")
    parsed = _extract_json(content)
    parsed.setdefault("executive_summary", "No summary generated.")
    parsed.setdefault("key_decisions", [])
    parsed.setdefault("action_items", [])
    parsed.setdefault("risks_flagged", [])
    parsed.setdefault("open_questions", [])
    parsed.setdefault("follow_up_email", {"subject": f"Follow-up: {meeting_title}", "body": ""})
    parsed["analysis_mode"] = "claude_api"
    return parsed


def transcribe_audio(audio_path: str | Path) -> str:
    """Transcribe audio locally using openai-whisper if installed."""
    try:
        import whisper  # type: ignore
    except ImportError as exc:
        raise RuntimeError("Audio transcription requires openai-whisper and ffmpeg. Install with: pip install openai-whisper") from exc
    model_name = os.getenv("WHISPER_MODEL", "base")
    model = whisper.load_model(model_name)
    result = model.transcribe(str(audio_path))
    return str(result.get("text", "")).strip()
