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


MEETING_TYPE_GUIDANCE = {
    "Project sync": "Focus on delivery progress, blockers, owners, dependencies, timeline risk, and next actions.",
    "Steering committee": "Focus on executive summary, decisions needed, escalations, RAG status, risks, and leadership asks.",
    "Incident review": "Focus on incident timeline, customer impact, root cause, remediation, owners, and prevention actions.",
    "Sprint planning": "Focus on sprint goal, backlog scope, dependencies, acceptance criteria, owners, and delivery risk.",
    "Vendor discussion": "Focus on vendor commitments, open commercial/technical questions, SLA risk, dependencies, and follow-up owners.",
    "Stakeholder workshop": "Focus on requirements, decisions, concerns, action items, open questions, and alignment gaps.",
}


def _get_api_key() -> str | None:
    """Read Anthropic API key from Streamlit secrets or environment."""
    try:
        import streamlit as st  # type: ignore

        key = st.secrets.get("ANTHROPIC_API_KEY") if hasattr(st, "secrets") else None
        if key:
            return str(key).strip()
    except Exception:
        pass
    key = os.getenv("ANTHROPIC_API_KEY")
    return key.strip() if key else None


def _fallback_analysis(
    transcript: str,
    meeting_title: str = "Meeting",
    reason: str = "no_api_key",
    meeting_type: str = "Project sync",
) -> Dict[str, Any]:
    """Deterministic fallback so the app remains demoable without a valid API key."""
    lines = [line.strip() for line in transcript.splitlines() if line.strip()]
    text = " ".join(lines)
    sentences = re.split(r"(?<=[.!?])\s+", text)
    actions: List[Dict[str, str]] = []
    decisions: List[str] = []
    risks: List[Dict[str, str]] = []
    questions: List[str] = []

    for s in sentences:
        lower = s.lower()
        clipped = s[:260]
        if any(k in lower for k in ["action", "follow up", "will", "owner", "deadline", "by friday", "by monday"]):
            actions.append(
                {
                    "owner": "TBD",
                    "action": clipped,
                    "due_date": "TBD",
                    "priority": "Medium",
                    "status": "Open",
                }
            )
        if any(k in lower for k in ["decided", "decision", "approved", "agreed", "we will"]):
            decisions.append(clipped)
        if any(k in lower for k in ["risk", "blocker", "issue", "delay", "concern", "dependency"]):
            risks.append(
                {
                    "risk": clipped,
                    "impact": "Medium",
                    "likelihood": "Medium",
                    "mitigation": "Clarify owner, timeline, and next escalation path.",
                    "owner": "TBD",
                }
            )
        if "?" in s or any(k in lower for k in ["open question", "clarify", "unknown"]):
            questions.append(clipped)

    summary_seed = " ".join(sentences[:3]) if sentences else "The meeting transcript was analyzed successfully."
    return {
        "meeting_type": meeting_type,
        "executive_summary": f"Demo-mode summary for {meeting_title}: {summary_seed[:650]}",
        "key_decisions": decisions[:5] or ["No explicit decisions detected in demo mode."],
        "action_items": actions[:8]
        or [
            {
                "owner": "TBD",
                "action": "Review the meeting notes and confirm next steps.",
                "due_date": "TBD",
                "priority": "Medium",
                "status": "Open",
            }
        ],
        "risks_flagged": risks[:5]
        or [
            {
                "risk": "No major risks detected in demo mode.",
                "impact": "Low",
                "likelihood": "Low",
                "mitigation": "Continue monitoring.",
                "owner": "TBD",
            }
        ],
        "open_questions": questions[:5] or ["No open questions detected in demo mode."],
        "pmo_status": {
            "rag_status": "Amber" if risks else "Green",
            "overall_health": "Needs follow-up" if actions or risks else "On track",
            "decision_needed": "Review action owners and deadlines.",
            "next_review": "Next project sync",
        },
        "follow_up_email": {
            "subject": f"Follow-up: {meeting_title}",
            "body": "Hi team,<br><br>Sharing a quick AI-generated meeting follow-up with summary, decisions, and next steps. Please review the action items and confirm any missing owners or deadlines.<br><br>Best regards,",
        },
        "analysis_mode": f"demo_fallback_{reason}",
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


def _ensure_list(value: Any) -> List[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _normalize_action_items(items: Any) -> List[Dict[str, str]]:
    normalized: List[Dict[str, str]] = []
    for item in _ensure_list(items):
        if isinstance(item, dict):
            normalized.append(
                {
                    "owner": str(item.get("owner") or "TBD"),
                    "action": str(item.get("action") or item.get("description") or item.get("summary") or "Review follow-up item"),
                    "due_date": str(item.get("due_date") or item.get("deadline") or "TBD"),
                    "priority": str(item.get("priority") or "Medium"),
                    "status": str(item.get("status") or "Open"),
                }
            )
        else:
            normalized.append(
                {
                    "owner": "TBD",
                    "action": str(item),
                    "due_date": "TBD",
                    "priority": "Medium",
                    "status": "Open",
                }
            )
    return normalized


def _normalize_risks(items: Any) -> List[Dict[str, str]]:
    normalized: List[Dict[str, str]] = []
    for item in _ensure_list(items):
        if isinstance(item, dict):
            normalized.append(
                {
                    "risk": str(item.get("risk") or item.get("description") or "Unspecified risk"),
                    "impact": str(item.get("impact") or "Medium"),
                    "likelihood": str(item.get("likelihood") or "Medium"),
                    "mitigation": str(item.get("mitigation") or "Define mitigation and owner."),
                    "owner": str(item.get("owner") or "TBD"),
                }
            )
        else:
            normalized.append(
                {
                    "risk": str(item),
                    "impact": "Medium",
                    "likelihood": "Medium",
                    "mitigation": "Define mitigation and owner.",
                    "owner": "TBD",
                }
            )
    return normalized


def analyze_meeting(
    transcript: str,
    meeting_title: str = "Meeting",
    participants: str = "",
    meeting_type: str = "Project sync",
) -> Dict[str, Any]:
    """Analyze a meeting transcript into structured PM-ready outputs."""
    if not transcript or len(transcript.strip()) < 20:
        raise ValueError("Please provide a longer meeting transcript.")

    api_key = _get_api_key()
    if not api_key or "your-api-key" in api_key or "your-real-key" in api_key:
        return _fallback_analysis(transcript, meeting_title, "missing_or_placeholder_api_key", meeting_type)

    try:
        from anthropic import Anthropic, AuthenticationError
    except ImportError as exc:
        raise RuntimeError("anthropic package is not installed. Run: pip install anthropic") from exc

    client = Anthropic(api_key=api_key)
    guidance = MEETING_TYPE_GUIDANCE.get(meeting_type, MEETING_TYPE_GUIDANCE["Project sync"])
    prompt = f"""
You are an expert AI Meeting Intelligence Agent for product, project, PMO, cloud operations, ITSM, and leadership teams.
Analyze the transcript and return ONLY valid JSON with this exact schema:
{{
  "meeting_type": "{meeting_type}",
  "executive_summary": "3-6 sentence leadership-ready summary",
  "key_decisions": ["decision with context"],
  "action_items": [
    {{
      "owner": "person/team or TBD",
      "action": "clear action description",
      "due_date": "date/deadline or TBD",
      "priority": "High/Medium/Low",
      "status": "Open/In progress/Blocked/Done"
    }}
  ],
  "risks_flagged": [
    {{
      "risk": "risk or blocker with context",
      "impact": "High/Medium/Low",
      "likelihood": "High/Medium/Low",
      "mitigation": "recommended mitigation",
      "owner": "person/team or TBD"
    }}
  ],
  "open_questions": ["open question or clarification needed"],
  "pmo_status": {{
    "rag_status": "Green/Amber/Red",
    "overall_health": "short PMO health statement",
    "decision_needed": "decision or escalation needed, or None",
    "next_review": "suggested next review cadence or meeting"
  }},
  "follow_up_email": {{
    "subject": "professional subject line",
    "body": "HTML-friendly follow-up email body with bullets and next steps"
  }}
}}

Meeting type guidance: {guidance}
Meeting title: {meeting_title or 'Meeting'}
Participants: {participants or 'Not provided'}
Transcript:
{transcript[:35000]}
"""

    try:
        response = client.messages.create(
            model=os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022"),
            max_tokens=3000,
            temperature=0.2,
            messages=[{"role": "user", "content": prompt}],
        )
    except AuthenticationError:
        return _fallback_analysis(transcript, meeting_title, "invalid_api_key", meeting_type)

    content = "".join(block.text for block in response.content if getattr(block, "type", None) == "text")
    parsed = _extract_json(content)
    parsed.setdefault("meeting_type", meeting_type)
    parsed.setdefault("executive_summary", "No summary generated.")
    parsed["key_decisions"] = _ensure_list(parsed.get("key_decisions"))
    parsed["action_items"] = _normalize_action_items(parsed.get("action_items"))
    parsed["risks_flagged"] = _normalize_risks(parsed.get("risks_flagged"))
    parsed["open_questions"] = _ensure_list(parsed.get("open_questions"))
    parsed.setdefault(
        "pmo_status",
        {
            "rag_status": "Amber" if parsed["risks_flagged"] else "Green",
            "overall_health": "Review generated actions and risks.",
            "decision_needed": "TBD",
            "next_review": "Next project sync",
        },
    )
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
