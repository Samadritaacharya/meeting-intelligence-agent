from __future__ import annotations

import html
import os
import tempfile
import time
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from utils.analyzer import analyze_meeting, transcribe_audio
from utils.exporter import (
    export_actions_to_jira_csv,
    export_risks_to_csv,
    export_to_docx,
    export_to_markdown,
    export_to_pdf,
)

load_dotenv()

st.set_page_config(
    page_title="Meeting Intelligence Agent",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get help": "https://github.com/Samadritaacharya/meeting-intelligence-agent",
        "Report a bug": "https://github.com/Samadritaacharya/meeting-intelligence-agent/issues",
        "About": "Independent AI meeting-to-PMO portfolio workflow.",
    },
)

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
* { font-family: Inter, system-ui, sans-serif; }
.stApp {
  background:
    radial-gradient(circle at 7% -5%, rgba(255,128,55,.18), transparent 31rem),
    radial-gradient(circle at 92% 3%, rgba(99,102,241,.12), transparent 34rem),
    linear-gradient(145deg,#090b13 0%,#11101b 48%,#0b0d16 100%);
  color:#f8f9fa;
}
.block-container { max-width:1460px; padding-top:1.15rem; padding-bottom:4rem; }
.hero {
  background:linear-gradient(122deg,rgba(21,22,35,.98) 0%,rgba(38,24,31,.98) 53%,rgba(103,43,24,.96) 100%);
  border:1px solid rgba(255,153,91,.18); border-radius:28px; padding:2.65rem 2.75rem;
  box-shadow:0 32px 100px rgba(0,0,0,.34); margin-bottom:1rem; position:relative; overflow:hidden;
}
.hero:before { content:''; position:absolute; inset:0; background:linear-gradient(110deg,transparent 0 59%,rgba(255,255,255,.04) 60%,transparent 61%); background-size:54px 100%; opacity:.36; }
.hero:after { content:''; position:absolute; width:430px; height:430px; border-radius:999px; right:-120px; top:-190px; background:rgba(255,120,55,.18); filter:blur(8px); }
.eyebrow { position:relative; z-index:2; color:#ffb67d; font-size:.75rem; letter-spacing:.14em; text-transform:uppercase; font-weight:800; margin-bottom:.72rem; }
.hero h1 { font-size:clamp(2.35rem,5vw,4.25rem); line-height:1; margin:0 0 .9rem; color:white; letter-spacing:-.06em; font-weight:800; position:relative; z-index:2; }
.hero p { font-size:1.06rem; line-height:1.72; max-width:980px; color:#d9dce7; margin:0; position:relative; z-index:2; }
.hero-chips { display:flex; flex-wrap:wrap; gap:.45rem; margin-top:1.2rem; position:relative; z-index:2; }
.hero-chip { display:inline-flex; align-items:center; gap:.42rem; padding:.36rem .7rem; border-radius:999px; background:rgba(255,255,255,.055); border:1px solid rgba(255,177,121,.16); color:#f8e8dd; font-size:.78rem; font-weight:650; backdrop-filter:blur(12px); }
.live-dot { width:.47rem; height:.47rem; border-radius:99px; background:#fb923c; box-shadow:0 0 0 5px rgba(251,146,60,.11); display:inline-block; }
.workflow-strip { display:grid; grid-template-columns:repeat(4,1fr); gap:.58rem; margin:.82rem 0 1.15rem; }
.workflow-step { background:rgba(255,255,255,.045); border:1px solid rgba(255,153,91,.14); border-radius:16px; padding:.86rem .95rem; box-shadow:0 12px 34px rgba(0,0,0,.15); }
.workflow-step strong { display:block; color:#fff0e6; font-size:.82rem; margin-bottom:.2rem; }
.workflow-step span { color:#969baa; font-size:.74rem; }
.workflow-step b { color:#fb923c; font-size:.69rem; margin-right:.25rem; }
.metric-card, .card { background:linear-gradient(180deg,rgba(255,255,255,.06),rgba(255,255,255,.035)); border:1px solid rgba(255,153,91,.16); border-radius:18px; padding:1.18rem; box-shadow:0 14px 38px rgba(0,0,0,.18); backdrop-filter:blur(14px); }
.metric-card { text-align:center; min-height:118px; display:grid; place-content:center; }
.metric-card .num { color:#ffb171; font-size:1.85rem; font-weight:800; letter-spacing:-.04em; }
.metric-card .label { color:#9ca3b5; font-size:.76rem; text-transform:uppercase; letter-spacing:.09em; margin-top:.28rem; }
.section-title { font-size:1.28rem; font-weight:800; color:#fff; margin:1.7rem 0 .8rem; display:flex; gap:.65rem; align-items:center; letter-spacing:-.02em; }
.section-title:before { content:''; width:5px; height:25px; border-radius:5px; background:linear-gradient(#ffc089,#f97316); }
.result-block { background:linear-gradient(135deg,rgba(255,128,55,.11),rgba(255,255,255,.035)); border:1px solid rgba(255,153,91,.16); border-radius:16px; padding:1rem 1.15rem; margin:.65rem 0; color:#f8fafc; }
.result-label { color:#ffb171; font-weight:800; text-transform:uppercase; letter-spacing:.09em; font-size:.72rem; margin-bottom:.35rem; }
.stButton>button, .stDownloadButton>button { border-radius:12px!important; background:linear-gradient(135deg,#fb923c,#f97316)!important; color:white!important; border:0!important; font-weight:800!important; box-shadow:0 12px 28px rgba(249,115,22,.20)!important; min-height:2.7rem; transition:transform .18s ease,box-shadow .18s ease!important; }
.stButton>button:hover, .stDownloadButton>button:hover { transform:translateY(-1px); box-shadow:0 16px 34px rgba(249,115,22,.28)!important; }
.stTabs [data-baseweb="tab-list"] { gap:.5rem; background:rgba(255,255,255,.04); border:1px solid rgba(255,153,91,.12); padding:.45rem; border-radius:16px; }
.stTabs [aria-selected="true"] { background:linear-gradient(135deg,#fb923c,#f97316); color:white; border-radius:12px; }
[data-testid="stSidebar"] { background:linear-gradient(180deg,#080911 0%,#12101a 100%); border-right:1px solid rgba(255,153,91,.14); }
[data-testid="stSidebar"] * { color:#ece8ed; }
[data-testid="stSidebar"] input, [data-testid="stSidebar"] [data-baseweb="select"] > div { background:rgba(255,255,255,.055)!important; border-color:rgba(255,153,91,.13)!important; }
div[data-testid="stMetric"] { background:linear-gradient(180deg,rgba(255,255,255,.06),rgba(255,255,255,.035)); border:1px solid rgba(255,153,91,.15); border-top:3px solid #fb923c; border-radius:16px; padding:14px 16px; }
div[data-testid="stMetricLabel"] { color:#a2a6b5; }
div[data-testid="stMetricValue"] { color:#fff7f2; letter-spacing:-.035em; }
div[data-testid="stExpander"] { background:rgba(255,255,255,.035); border:1px solid rgba(255,153,91,.12); border-radius:15px; }
div[data-testid="stDataFrame"] { border:1px solid rgba(255,153,91,.12); border-radius:14px; overflow:hidden; }
textarea { background:rgba(255,255,255,.045)!important; border-color:rgba(255,153,91,.13)!important; }
.small { color:#a8adbb; font-size:.9rem; }
.template-chip { display:inline-block; background:rgba(255,161,94,.10); border:1px solid rgba(255,177,121,.18); padding:.42rem .68rem; border-radius:12px; margin:.15rem 0; color:#ffd4b3; font-size:.8rem; line-height:1.45; }
.footer-note { margin-top:2rem; color:#747b8b; font-size:.8rem; text-align:center; }
@media(max-width:900px){.workflow-strip{grid-template-columns:1fr 1fr}.hero{padding:2rem 1.45rem}}
@media(max-width:560px){.workflow-strip{grid-template-columns:1fr}}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

MEETING_TYPES = [
    "Project sync",
    "Steering committee",
    "Incident review",
    "Sprint planning",
    "Vendor discussion",
    "Stakeholder workshop",
]

PMO_TEMPLATES = {
    "Project sync": "Progress, blockers, owners, dependencies, timeline risk, and next actions.",
    "Steering committee": "Executive summary, RAG status, decisions needed, risks, escalations, and leadership asks.",
    "Incident review": "Timeline, impact, root cause, remediation, prevention actions, and accountable owners.",
    "Sprint planning": "Sprint goal, backlog scope, acceptance criteria, dependencies, and delivery risk.",
    "Vendor discussion": "Commitments, SLA questions, dependencies, commercial/technical follow-ups, and owners.",
    "Stakeholder workshop": "Requirements, decisions, concerns, action items, open questions, and alignment gaps.",
}


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


def as_list(value: Any) -> List[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def action_rows(result: Dict[str, Any]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for item in as_list(result.get("action_items")):
        if isinstance(item, dict):
            rows.append(
                {
                    "Owner": str(item.get("owner") or "TBD"),
                    "Action": str(item.get("action") or item.get("description") or item.get("summary") or "Review follow-up item"),
                    "Due Date": str(item.get("due_date") or item.get("deadline") or "TBD"),
                    "Priority": str(item.get("priority") or "Medium"),
                    "Status": str(item.get("status") or "Open"),
                }
            )
        else:
            rows.append({"Owner": "TBD", "Action": str(item), "Due Date": "TBD", "Priority": "Medium", "Status": "Open"})
    return rows


def risk_rows(result: Dict[str, Any]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for item in as_list(result.get("risks_flagged")):
        if isinstance(item, dict):
            rows.append(
                {
                    "Risk": str(item.get("risk") or item.get("description") or "Unspecified risk"),
                    "Impact": str(item.get("impact") or "Medium"),
                    "Likelihood": str(item.get("likelihood") or "Medium"),
                    "Mitigation": str(item.get("mitigation") or "Define mitigation and owner."),
                    "Owner": str(item.get("owner") or "TBD"),
                }
            )
        else:
            rows.append(
                {
                    "Risk": str(item),
                    "Impact": "Medium",
                    "Likelihood": "Medium",
                    "Mitigation": "Define mitigation and owner.",
                    "Owner": "TBD",
                }
            )
    return rows


if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "transcript" not in st.session_state:
    st.session_state.transcript = ""

st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">AI Meeting Workflow · PMO Copilot · Structured Follow-through</div>
      <h1>Meeting Intelligence Agent</h1>
      <p>Transform a raw transcript into a leadership-ready operating package: executive summary, decisions, owners, risks, open questions, follow-up communication and exportable PMO artefacts.</p>
      <div class="hero-chips"><span class="hero-chip"><span class="live-dot"></span> Claude + deterministic demo mode</span><span class="hero-chip">6 PMO templates</span><span class="hero-chip">Structured actions</span><span class="hero-chip">PDF · DOCX · CSV · MD</span></div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="workflow-strip">
      <div class="workflow-step"><strong><b>01</b> Capture</strong><span>Transcript or optional audio</span></div>
      <div class="workflow-step"><strong><b>02</b> Structure</strong><span>Summary, decisions, risks, actions</span></div>
      <div class="workflow-step"><strong><b>03</b> Align</strong><span>RAG, owners, questions, follow-up</span></div>
      <div class="workflow-step"><strong><b>04</b> Export</strong><span>PMO-ready reusable artefacts</span></div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("### ✦ Meeting workspace")
    st.caption("Set the meeting context first; the analysis adapts to the PMO template.")
    meeting_title = st.text_input("Meeting title", value="Product Strategy Sync")
    participants = st.text_input("Participants", value="Product, Engineering, Operations")
    meeting_type = st.selectbox("PMO template", MEETING_TYPES, index=0)
    st.markdown(f'<span class="template-chip">{esc(PMO_TEMPLATES[meeting_type])}</span>', unsafe_allow_html=True)
    st.divider()
    api_present = bool(get_secret("ANTHROPIC_API_KEY"))
    if api_present:
        st.success("Claude API · connected")
    else:
        st.info("Demo mode · no API key required")
    st.markdown("### Privacy by design")
    st.caption("No secrets are stored in GitHub. Use .env locally or Streamlit Secrets in deployment.")

col_a, col_b, col_c, col_d = st.columns(4)
for col, num, label in [
    (col_a, "6", "PMO templates"),
    (col_b, "JSON", "Structured output"),
    (col_c, "5", "Export formats"),
    (col_d, "Safe", "Secrets isolated"),
]:
    with col:
        st.markdown(f'<div class="metric-card"><div class="num">{num}</div><div class="label">{label}</div></div>', unsafe_allow_html=True)

st.markdown('<div class="section-title">Bring in the meeting</div>', unsafe_allow_html=True)
tab1, tab2, tab3 = st.tabs(["Paste transcript", "Upload audio", "Instant sample"])

with tab1:
    transcript = st.text_area(
        "Meeting transcript",
        value=st.session_state.transcript,
        height=280,
        placeholder="Paste a meeting transcript here...",
    )
    if st.button("Analyze transcript →", use_container_width=True):
        with st.spinner("Structuring the meeting into PMO outputs..."):
            try:
                st.session_state.analysis_result = analyze_meeting(transcript, meeting_title, participants, meeting_type)
                st.session_state.transcript = transcript
                st.success("Analysis complete")
            except Exception as exc:
                st.error(f"Analysis failed: {exc}")

with tab2:
    st.markdown('<div class="card"><b>Optional audio workflow</b><br><span class="small">Audio transcription requires openai-whisper and ffmpeg installed locally or in the deployment environment.</span></div>', unsafe_allow_html=True)
    audio = st.file_uploader("Upload audio", type=["mp3", "wav", "m4a", "mp4"])
    if audio and st.button("Transcribe & analyze →", use_container_width=True):
        suffix = Path(audio.name).suffix or ".mp3"
        tmp_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(audio.read())
                tmp_path = tmp.name
            with st.spinner("Transcribing audio locally..."):
                transcript = transcribe_audio(tmp_path)
                st.session_state.transcript = transcript
            with st.spinner("Structuring the meeting into PMO outputs..."):
                st.session_state.analysis_result = analyze_meeting(transcript, meeting_title, participants, meeting_type)
            st.success("Audio analyzed")
        except Exception as exc:
            st.error(str(exc))
        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.remove(tmp_path)

with tab3:
    st.markdown('<div class="card"><b>Recruiter demo</b><br><span class="small">Load a synthetic meeting and test the complete workflow in one click.</span></div>', unsafe_allow_html=True)
    if st.button("Run sample workflow →", use_container_width=True):
        sample_path = Path("sample_data/sample_transcript.txt")
        if not sample_path.exists():
            st.error("Sample transcript not found")
        else:
            sample = sample_path.read_text(encoding="utf-8")
            with st.spinner("Generating PMO outputs from the sample..."):
                st.session_state.transcript = sample
                st.session_state.analysis_result = analyze_meeting(sample, "FinTrack Berlin - Q2 Planning", "Elena, Marcus, Sarah, Priya", meeting_type)
            st.success("Sample analysis complete")

result = st.session_state.analysis_result
if result:
    st.markdown('<div class="section-title">Decision package</div>', unsafe_allow_html=True)
    mode = result.get("analysis_mode")
    if mode and mode != "claude_api":
        st.info("Deterministic demo/fallback mode is active. Add a valid Anthropic API key for live Claude analysis.")

    pmo_status = result.get("pmo_status", {}) or {}
    if pmo_status:
        st.markdown('<div class="section-title">PMO pulse</div>', unsafe_allow_html=True)
        s1, s2, s3, s4 = st.columns(4)
        s1.metric("RAG Status", pmo_status.get("rag_status", "TBD"))
        s2.metric("Overall Health", pmo_status.get("overall_health", "TBD"))
        s3.metric("Decision Needed", pmo_status.get("decision_needed", "TBD"))
        s4.metric("Next Review", pmo_status.get("next_review", "TBD"))

    with st.expander("Executive summary", expanded=True):
        st.markdown(f'<div class="result-block"><div class="result-label">Leadership summary</div>{esc(result.get("executive_summary"))}</div>', unsafe_allow_html=True)

    decisions = as_list(result.get("key_decisions"))
    actions = action_rows(result)
    risks = risk_rows(result)
    questions = as_list(result.get("open_questions"))

    col1, col2 = st.columns(2)
    with col1:
        with st.expander(f"Key decisions · {len(decisions)}", expanded=True):
            for i, item in enumerate(decisions, 1):
                st.markdown(f'<div class="result-block"><div class="result-label">Decision {i}</div>{esc(item)}</div>', unsafe_allow_html=True)
        with st.expander(f"Risk register · {len(risks)}", expanded=True):
            if risks:
                st.dataframe(pd.DataFrame(risks), use_container_width=True, hide_index=True)
            else:
                st.caption("No risks detected.")
    with col2:
        with st.expander(f"Owner action table · {len(actions)}", expanded=True):
            if actions:
                st.dataframe(pd.DataFrame(actions), use_container_width=True, hide_index=True)
            else:
                st.caption("No action items detected.")
        with st.expander(f"Open questions · {len(questions)}", expanded=False):
            for item in questions:
                st.markdown(f'<div class="result-block">{esc(item)}</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Follow-up communication</div>', unsafe_allow_html=True)
    email = result.get("follow_up_email", {}) or {}
    st.markdown(
        f'<div class="card"><b style="color:#ffb171;">Subject:</b> {esc(email.get("subject"))}<br><br>{safe_email_body(email.get("body"))}</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-title">Export the operating record</div>', unsafe_allow_html=True)
    e1, e2, e3, e4 = st.columns(4)
    timestamp = int(time.time())
    with e1:
        try:
            pdf = export_to_pdf(result)
            st.download_button("PDF report", data=pdf, file_name=f"meeting_report_{timestamp}.pdf", mime="application/pdf", use_container_width=True)
        except Exception as exc:
            st.error(f"PDF export unavailable: {exc}")
    with e2:
        try:
            docx = export_to_docx(result)
            st.download_button("DOCX report", data=docx, file_name=f"meeting_report_{timestamp}.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)
        except Exception as exc:
            st.error(f"DOCX export unavailable: {exc}")
    with e3:
        try:
            jira_csv = export_actions_to_jira_csv(result)
            st.download_button("Jira action CSV", data=jira_csv, file_name=f"jira_action_items_{timestamp}.csv", mime="text/csv", use_container_width=True)
        except Exception as exc:
            st.error(f"CSV export unavailable: {exc}")
    with e4:
        try:
            markdown = export_to_markdown(result)
            st.download_button("Notion / Markdown", data=markdown, file_name=f"meeting_notes_{timestamp}.md", mime="text/markdown", use_container_width=True)
        except Exception as exc:
            st.error(f"Markdown export unavailable: {exc}")

    r1, _ = st.columns([1, 3])
    with r1:
        try:
            risk_csv = export_risks_to_csv(result)
            st.download_button("Risk register CSV", data=risk_csv, file_name=f"risk_register_{timestamp}.csv", mime="text/csv", use_container_width=True)
        except Exception as exc:
            st.error(f"Risk export unavailable: {exc}")

st.markdown('<div class="footer-note">Meeting Intelligence Agent · independent portfolio project · synthetic sample data · PMO-ready workflow automation</div>', unsafe_allow_html=True)
