from __future__ import annotations

import html
import os
import tempfile
import time
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from utils.analyzer import analyze_meeting, transcribe_audio
from utils.exporter import export_to_docx, export_to_pdf

load_dotenv()

st.set_page_config(
    page_title="Meeting Intelligence Agent",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
* { font-family: Inter, system-ui, sans-serif; }
.stApp { background: radial-gradient(circle at top left, rgba(255,140,66,.20), transparent 32%), linear-gradient(135deg,#0f0f1e 0%,#181225 55%,#0f111a 100%); color:#f8f9fa; }
.hero { background: linear-gradient(135deg,#ff9f45 0%,#ff6b35 48%,#e85d04 100%); border-radius: 28px; padding: 3.2rem 2.7rem; box-shadow: 0 28px 90px rgba(255,107,53,.30); margin-bottom: 2rem; position:relative; overflow:hidden; }
.hero:after { content:''; position:absolute; width:380px; height:380px; border-radius:999px; right:-90px; top:-120px; background:rgba(255,255,255,.18); filter:blur(80px); }
.hero h1 { font-size: clamp(2.2rem, 5vw, 4.4rem); line-height:1; margin:0 0 .9rem; color:white; letter-spacing:-.06em; font-weight:800; position:relative; z-index:2; }
.hero p { font-size:1.15rem; max-width:900px; color:rgba(255,255,255,.94); margin:0; position:relative; z-index:2; }
.metric-card, .card { background: rgba(255,255,255,.055); border:1px solid rgba(255,140,66,.24); border-radius:18px; padding:1.25rem; box-shadow:0 12px 35px rgba(0,0,0,.22); backdrop-filter: blur(14px); }
.metric-card { text-align:center; }
.metric-card .num { color:#ffb86b; font-size:2rem; font-weight:800; }
.metric-card .label { color:#cbd5e1; font-size:.88rem; text-transform:uppercase; letter-spacing:.08em; }
.section-title { font-size:1.35rem; font-weight:800; color:#fff; margin: 1.7rem 0 .8rem; display:flex; gap:.65rem; align-items:center; }
.section-title:before { content:''; width:5px; height:27px; border-radius:5px; background:linear-gradient(#ffb86b,#ff6b35); }
.result-block { background:linear-gradient(135deg,rgba(255,140,66,.13),rgba(255,255,255,.045)); border:1px solid rgba(255,140,66,.24); border-radius:16px; padding:1rem 1.15rem; margin:.65rem 0; color:#f8fafc; }
.result-label { color:#ffb86b; font-weight:800; text-transform:uppercase; letter-spacing:.08em; font-size:.74rem; margin-bottom:.35rem; }
.stButton>button, .stDownloadButton>button { border-radius:12px!important; background:linear-gradient(135deg,#ff9f45,#ff6b35)!important; color:white!important; border:0!important; font-weight:800!important; box-shadow:0 12px 28px rgba(255,107,53,.28)!important; }
.stTabs [data-baseweb="tab-list"] { gap:.5rem; background:rgba(255,140,66,.08); border:1px solid rgba(255,140,66,.15); padding:.45rem; border-radius:16px; }
.stTabs [aria-selected="true"] { background:linear-gradient(135deg,#ff9f45,#ff6b35); color:white; border-radius:12px; }
[data-testid="stSidebar"] { background:rgba(12,13,24,.78); border-right:1px solid rgba(255,140,66,.18); }
.small { color:#cbd5e1; font-size:.92rem; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


def esc(value: object) -> str:
    return html.escape(str(value or ""))


def safe_email_body(value: object) -> str:
    escaped = esc(value)
    return escaped.replace("&lt;br&gt;", "<br>").replace("&lt;br/&gt;", "<br>").replace("&lt;br /&gt;", "<br>")


def get_secret(name: str) -> str | None:
    try:
        value = st.secrets.get(name)
        if value:
            return str(value)
    except Exception:
        pass
    return os.getenv(name)


if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "transcript" not in st.session_state:
    st.session_state.transcript = ""

st.markdown(
    """
    <div class="hero">
      <h1>🎙️ Meeting Intelligence Agent</h1>
      <p>Convert raw meeting transcripts into executive summaries, key decisions, action items, risks, open questions, and ready-to-send follow-up emails — powered by Claude.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("## ⚙️ Meeting setup")
    meeting_title = st.text_input("Meeting title", value="Product Strategy Sync")
    participants = st.text_input("Participants", value="Product, Engineering, Operations")
    st.markdown("---")
    api_present = bool(get_secret("ANTHROPIC_API_KEY"))
    if api_present:
        st.success("Claude API key detected")
    else:
        st.info("Demo mode: add ANTHROPIC_API_KEY for Claude analysis")
    st.markdown("### 🔐 Privacy")
    st.caption("No secrets are stored in GitHub. Use .env locally or Streamlit Secrets in deployment.")

col_a, col_b, col_c, col_d = st.columns(4)
for col, num, label in [
    (col_a, "10s", "Analysis target"),
    (col_b, "JSON", "Structured output"),
    (col_c, "PDF/DOCX", "Export ready"),
    (col_d, "Secure", "Secrets safe"),
]:
    with col:
        st.markdown(f'<div class="metric-card"><div class="num">{num}</div><div class="label">{label}</div></div>', unsafe_allow_html=True)

st.markdown('<div class="section-title">Input</div>', unsafe_allow_html=True)
tab1, tab2, tab3 = st.tabs(["📝 Paste transcript", "🎵 Upload audio", "📄 Load sample"])

with tab1:
    transcript = st.text_area(
        "Paste your meeting transcript",
        value=st.session_state.transcript,
        height=280,
        placeholder="Paste a meeting transcript here...",
    )
    if st.button("✨ Analyze transcript", use_container_width=True):
        with st.spinner("Analyzing meeting..."):
            try:
                st.session_state.analysis_result = analyze_meeting(transcript, meeting_title, participants)
                st.session_state.transcript = transcript
                st.success("Analysis complete")
            except Exception as exc:
                st.error(f"Analysis failed: {exc}")

with tab2:
    st.markdown('<div class="card"><b>Optional audio mode</b><br><span class="small">Audio transcription requires openai-whisper and ffmpeg installed locally or in the deployment environment.</span></div>', unsafe_allow_html=True)
    audio = st.file_uploader("Upload audio", type=["mp3", "wav", "m4a", "mp4"])
    if audio and st.button("🎧 Transcribe and analyze", use_container_width=True):
        suffix = Path(audio.name).suffix or ".mp3"
        tmp_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(audio.read())
                tmp_path = tmp.name
            with st.spinner("Transcribing audio locally..."):
                transcript = transcribe_audio(tmp_path)
                st.session_state.transcript = transcript
            with st.spinner("Analyzing transcript..."):
                st.session_state.analysis_result = analyze_meeting(transcript, meeting_title, participants)
            st.success("Audio analyzed")
        except Exception as exc:
            st.error(str(exc))
        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.remove(tmp_path)

with tab3:
    st.markdown('<div class="card"><b>Portfolio demo</b><br><span class="small">Use the sample transcript to test the full workflow immediately.</span></div>', unsafe_allow_html=True)
    if st.button("▶️ Load and analyze sample", use_container_width=True):
        sample_path = Path("sample_data/sample_transcript.txt")
        if not sample_path.exists():
            st.error("Sample transcript not found")
        else:
            sample = sample_path.read_text(encoding="utf-8")
            with st.spinner("Analyzing sample meeting..."):
                st.session_state.transcript = sample
                st.session_state.analysis_result = analyze_meeting(sample, "FinTrack Berlin - Q2 Planning", "Elena, Marcus, Sarah, Priya")
            st.success("Sample analysis complete")

result = st.session_state.analysis_result
if result:
    st.markdown('<div class="section-title">Analysis results</div>', unsafe_allow_html=True)
    mode = result.get("analysis_mode")
    if mode and mode != "claude_api":
        st.info("Demo/fallback mode is active. Add a valid Anthropic API key for live Claude analysis.")

    with st.expander("📋 Executive Summary", expanded=True):
        st.markdown(f'<div class="result-block"><div class="result-label">Summary</div>{esc(result.get("executive_summary"))}</div>', unsafe_allow_html=True)

    decisions = result.get("key_decisions", []) or []
    actions = result.get("action_items", []) or []
    risks = result.get("risks_flagged", []) or []
    questions = result.get("open_questions", []) or []

    col1, col2 = st.columns(2)
    with col1:
        with st.expander(f"✅ Key Decisions ({len(decisions)})", expanded=True):
            for i, item in enumerate(decisions, 1):
                st.markdown(f'<div class="result-block"><div class="result-label">Decision {i}</div>{esc(item)}</div>', unsafe_allow_html=True)
        with st.expander(f"⚠️ Risks ({len(risks)})", expanded=False):
            for item in risks:
                st.markdown(f'<div class="result-block">{esc(item)}</div>', unsafe_allow_html=True)
    with col2:
        with st.expander(f"🎯 Action Items ({len(actions)})", expanded=True):
            for i, item in enumerate(actions, 1):
                st.markdown(f'<div class="result-block"><div class="result-label">Action {i}</div>{esc(item)}</div>', unsafe_allow_html=True)
        with st.expander(f"❓ Open Questions ({len(questions)})", expanded=False):
            for item in questions:
                st.markdown(f'<div class="result-block">{esc(item)}</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Follow-up email</div>', unsafe_allow_html=True)
    email = result.get("follow_up_email", {}) or {}
    st.markdown(
        f'<div class="card"><b style="color:#ffb86b;">Subject:</b> {esc(email.get("subject"))}<br><br>{safe_email_body(email.get("body"))}</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-title">Export</div>', unsafe_allow_html=True)
    e1, e2 = st.columns(2)
    with e1:
        try:
            pdf = export_to_pdf(result)
            st.download_button("📄 Download PDF", data=pdf, file_name=f"meeting_report_{int(time.time())}.pdf", mime="application/pdf", use_container_width=True)
        except Exception as exc:
            st.error(f"PDF export unavailable: {exc}")
    with e2:
        try:
            docx = export_to_docx(result)
            st.download_button("📝 Download DOCX", data=docx, file_name=f"meeting_report_{int(time.time())}.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)
        except Exception as exc:
            st.error(f"DOCX export unavailable: {exc}")

st.caption("Built by Samadrita Acharya · AI portfolio project · Claude API + Streamlit + Python")
