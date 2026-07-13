import streamlit as st
import requests

# ─────────────────────────────────────────────
# 1. Page Config
# ─────────────────────────────────────────────
st.set_page_config(page_title="MLH Demo Pitch Generator", page_icon="🎤", layout="wide")

BACKEND_URL = "https://demo-pitch-generator-api.onrender.com/generate-pitch"


# Streamlit renders any line indented 4+ spaces as a code block.
# This collapses HTML so no line has leading whitespace -> renders as real HTML.
def html(markup: str):
    cleaned = "".join(line.strip() for line in markup.strip().splitlines())
    st.markdown(cleaned, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 2. Global CSS  (DARK THEME)
# ─────────────────────────────────────────────
st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #0B1120 0%, #0F172A 45%, #111827 100%);
    background-attachment: fixed;
}
#MainMenu, footer { visibility: hidden; }

/* Sidebar */
section[data-testid="stSidebar"] { background-color: #0B1120; border-right: 1px solid #1E293B; }
section[data-testid="stSidebar"] * { color: #E5E7EB !important; }
section[data-testid="stSidebar"] .stTextInput input {
    background-color: #1E293B; border: 1px solid #334155; color: #F9FAFB !important;
}
div[data-testid="InputInstructions"] { display: none; }

/* Spinner text — light so it shows on dark */
div[data-testid="stSpinner"] p, .stSpinner > div > div {
    color: #E2E8F0 !important; font-weight: 600;
}

/* Hero */
.hero {
    background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
    border-radius: 16px; padding: 26px 32px; margin-bottom: 24px; color: white;
    box-shadow: 0 8px 24px rgba(79,70,229,0.25);
}
.hero-label {
    text-transform: uppercase; font-size: 12px; letter-spacing: 1.5px;
    opacity: 0.9; margin-bottom: 4px;
}
.hero-title { font-size: 28px; font-weight: 800; margin: 0; color: #FFFFFF; }

/* Cards */
.card {
    background: #1E293B; border: 1px solid #334155; border-radius: 14px;
    padding: 20px 22px; height: 100%; box-shadow: 0 2px 8px rgba(0,0,0,0.25);
}
.card-header { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; }
.card-icon {
    font-size: 20px; width: 36px; height: 36px; border-radius: 9px;
    display: flex; align-items: center; justify-content: center;
}
.icon-hook { background: rgba(59,130,246,0.15); }
.icon-problem { background: rgba(239,68,68,0.15); }
.icon-wow { background: rgba(16,185,129,0.15); }
.card-title {
    font-weight: 700; font-size: 14px; color: #94A3B8;
    text-transform: uppercase; letter-spacing: 0.5px;
}
.card-time {
    margin-left: auto; font-size: 12px; font-weight: 700; color: #C7D2FE;
    background: rgba(99,102,241,0.18); padding: 2px 10px; border-radius: 999px;
}
.card-body { font-size: 16px; line-height: 1.55; color: #E2E8F0; word-wrap: break-word; }

/* Wow card */
.wow-card {
    background: linear-gradient(135deg, #0F2A22 0%, #10231C 100%);
    border: 1px solid #14532D;
}
.wow-card .card-body { color: #D1FAE5; }

/* Timeline */
.timeline-item { display: flex; gap: 16px; position: relative; padding-bottom: 26px; }
.timeline-item:last-child { padding-bottom: 0; }
.timeline-rail { display: flex; flex-direction: column; align-items: center; width: 24px; }
.timeline-dot {
    width: 12px; height: 12px; border-radius: 50%; background: #818CF8;
    flex-shrink: 0; margin-top: 4px; box-shadow: 0 0 0 3px rgba(129,140,248,0.2);
}
.timeline-line { width: 2px; flex-grow: 1; background: #334155; margin-top: 4px; }
.timeline-content { flex: 1; }
.timeline-time {
    display: inline-block; background: rgba(99,102,241,0.18); color: #C7D2FE;
    font-size: 12px; font-weight: 700; padding: 2px 10px; border-radius: 999px;
    margin-bottom: 6px;
}
.timeline-action { font-weight: 700; color: #F1F5F9; margin-bottom: 6px; font-size: 15px; }
.timeline-script {
    color: #CBD5E1; font-size: 14px; line-height: 1.5; font-style: italic;
    background: #0F172A; border-left: 3px solid #4F46E5; padding: 8px 12px;
    border-radius: 6px; word-wrap: break-word;
}

/* Warnings */
.warn-item {
    display: flex; gap: 12px; align-items: flex-start; background: rgba(245,158,11,0.10);
    border: 1px solid rgba(245,158,11,0.35); border-radius: 10px; padding: 12px 14px;
    margin-bottom: 10px;
}
.warn-item:last-child { margin-bottom: 0; }
.warn-icon { font-size: 18px; flex-shrink: 0; }
.warn-text { color: #FCD34D; font-size: 14px; line-height: 1.5; word-wrap: break-word; }

/* Section subheadings + info box text */
h4, .stMarkdown h4 { color: #E2E8F0 !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 3. Sidebar
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎤 Pitch Generator")
    st.caption("Just finished 36 hours of coding? Drop your repo and get a 2-minute winning pitch.")
    st.markdown("---")
    repo_url = st.text_input("Public GitHub Repository URL", placeholder="https://github.com/psf/requests")
    submit = st.button("✨ Generate Pitch", use_container_width=True, type="primary")
    st.markdown("---")
    st.caption("⏳ First run may take 30–50s while the server wakes up.")

# ─────────────────────────────────────────────
# 4. Main App
# ─────────────────────────────────────────────
html(
    "<h1 style='font-weight:800;color:#F8FAFC;margin-bottom:0;'>MLH Demo Pitch Generator</h1>"
    "<p style='color:#94A3B8;margin-top:4px;'>AI writes your 2-minute winning presentation from any GitHub repo.</p>"
)
st.write("")


def card(icon, icon_class, title, body, time=None):
    time_html = f'<div class="card-time">{time}</div>' if time else ""
    return (
        f'<div class="card">'
        f'<div class="card-header">'
        f'<div class="card-icon {icon_class}">{icon}</div>'
        f'<div class="card-title">{title}</div>'
        f'{time_html}'
        f'</div>'
        f'<div class="card-body">{body}</div>'
        f'</div>'
    )


if submit:
    if not repo_url:
        st.warning("Please enter a GitHub URL first.")
    else:
        with st.spinner("Server waking up (30–50s) & AI writing your pitch..."):
            try:
                response = requests.post(BACKEND_URL, json={"repo_url": repo_url}, timeout=120)

                if response.status_code == 200:
                    pitch = response.json()

                    # Hero
                    html(
                        f'<div class="hero">'
                        f'<div class="hero-label">Pitch Generated For</div>'
                        f'<p class="hero-title">{pitch["project_name"]}</p>'
                        f'</div>'
                    )

                    # Hook + Problem
                    col1, col2 = st.columns(2)
                    with col1:
                        html(card("🪝", "icon-hook", "The Hook", pitch["hook"], time="0:00 – 0:15"))
                    with col2:
                        html(card("🚩", "icon-problem", "The Problem", pitch["problem_statement"]))

                    st.write("")

                    # Wow Moment
                    html(
                        f'<div class="card wow-card">'
                        f'<div class="card-header">'
                        f'<div class="card-icon icon-wow">✨</div>'
                        f'<div class="card-title">The "Wow" Moment</div>'
                        f'</div>'
                        f'<div class="card-body">{pitch["wow_moment"]}</div>'
                        f'</div>'
                    )

                    st.write("")
                    st.markdown("#### ⏱️ 2-Minute Script Timeline")

                    # Timeline
                    n = len(pitch["timeline"])
                    timeline = ""
                    for i, seg in enumerate(pitch["timeline"]):
                        line = '<div class="timeline-line"></div>' if i < n - 1 else ""
                        timeline += (
                            f'<div class="timeline-item">'
                            f'<div class="timeline-rail"><div class="timeline-dot"></div>{line}</div>'
                            f'<div class="timeline-content">'
                            f'<div class="timeline-time">{seg["time_marker"]}</div>'
                            f'<div class="timeline-action">📺 {seg["action"]}</div>'
                            f'<div class="timeline-script">🗣️ "{seg["talking_points"]}"</div>'
                            f'</div>'
                            f'</div>'
                        )
                    html(f'<div class="card">{timeline}</div>')

                    # Demo Warnings
                    if pitch.get("demo_warnings"):
                        st.write("")
                        st.markdown("#### ⚠️ Demo Warnings")
                        warns = ""
                        for w in pitch["demo_warnings"]:
                            warns += (
                                f'<div class="warn-item">'
                                f'<div class="warn-icon">⚠️</div>'
                                f'<div class="warn-text">{w}</div>'
                                f'</div>'
                            )
                        html(warns)

                elif response.status_code == 502:
                    st.error("The server is still waking up. Please wait 10 seconds and try generating again!")
                else:
                    detail = response.json().get("detail", "Unknown error")
                    st.error(f"Failed to generate pitch. Error: {detail}")

            except requests.exceptions.Timeout:
                st.error("The request timed out. The server is taking too long to respond. Please try again!")
            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to the backend server. Please check the URL.")
            except Exception as e:
                st.error(f"Something went wrong: {e}")
else:
    st.info("👈 Paste a public GitHub repository URL in the sidebar and hit **Generate Pitch** to get started.")