import pytest

from utils.analyzer import _extract_json, analyze_meeting


SAMPLE_TRANSCRIPT = """
The team agreed to release the pilot next Monday.
Priya will confirm the monitoring owner by Friday.
A dependency on the vendor API may delay testing.
Do we need a separate security review?
"""


def test_demo_fallback_returns_structured_output(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_MODEL", raising=False)

    result = analyze_meeting(
        SAMPLE_TRANSCRIPT,
        meeting_title="Pilot Planning",
        participants="Priya, Engineering, PMO",
        meeting_type="Project sync",
    )

    assert result["analysis_mode"].startswith("demo_fallback_")
    assert result["meeting_type"] == "Project sync"
    assert result["executive_summary"]
    assert result["key_decisions"]
    assert result["action_items"]
    assert result["risks_flagged"]
    assert result["open_questions"]
    assert result["pmo_status"]["rag_status"] in {"Green", "Amber", "Red"}


def test_missing_model_configuration_uses_safe_fallback(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.delenv("ANTHROPIC_MODEL", raising=False)

    result = analyze_meeting(SAMPLE_TRANSCRIPT, meeting_title="Model Configuration Test")

    assert result["analysis_mode"] == "demo_fallback_missing_model_configuration"


def test_short_transcript_is_rejected():
    with pytest.raises(ValueError, match="longer meeting transcript"):
        analyze_meeting("Too short")


def test_extract_json_accepts_markdown_code_fence():
    parsed = _extract_json('```json\n{"status": "ok"}\n```')
    assert parsed == {"status": "ok"}
