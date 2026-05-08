import streamlit as st
import google.generativeai as genai

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Job Description Optimizer",
    page_icon="🎯",
    layout="centered"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0f1117; }
    .stTextArea textarea {
        background-color: #1e2130;
        color: white;
        border: 1px solid #3d4166;
        border-radius: 10px;
        font-size: 14px;
    }
    .stTextInput input {
        background-color: #1e2130;
        color: white;
        border: 1px solid #3d4166;
        border-radius: 10px;
    }
    .result-box {
        background-color: #1e2130;
        border: 1px solid #3d4166;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
    }
    .section-title {
        color: #7c83f7;
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 10px;
    }
    .bullet-item {
        background-color: #252840;
        border-left: 3px solid #7c83f7;
        padding: 10px 15px;
        border-radius: 0 8px 8px 0;
        margin: 6px 0;
        color: #e0e0e0;
        font-size: 14px;
        line-height: 1.6;
    }
    .keyword-chip {
        display: inline-block;
        background-color: #2d3561;
        color: #a0a8ff;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        margin: 3px;
        border: 1px solid #4a52a0;
    }
    .cover-box {
        background-color: #1a2a1a;
        border: 1px solid #2d5a2d;
        border-radius: 12px;
        padding: 20px;
        color: #c8f0c8;
        font-size: 14px;
        line-height: 1.7;
    }
    .tip-box {
        background-color: #2a1f1a;
        border: 1px solid #5a3d2d;
        border-radius: 12px;
        padding: 15px 20px;
        color: #f0d0b0;
        font-size: 13px;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 30px;
        font-size: 16px;
        font-weight: 600;
        width: 100%;
        cursor: pointer;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #764ba2, #667eea);
    }
    h1 { color: #ffffff !important; }
    h2, h3 { color: #a0a8ff !important; }
    .stMarkdown p { color: #c0c0c0; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("# 🎯 AI Job Description Optimizer")
st.markdown("**Paste any job description → Get tailored resume bullets + cover letter angle in seconds**")
st.markdown("---")

# ── API Key input ─────────────────────────────────────────────────────────────
st.markdown("### 🔑 Step 1: Enter your Gemini API Key")
api_key = st.text_input(
    "Your Google Gemini API Key",
    type="password",
    placeholder="Paste your API key here (starts with AIza...)",
    help="Get your free key at aistudio.google.com"
)

st.markdown("### 📋 Step 2: Paste the Job Description")
jd_input = st.text_area(
    "Job Description",
    height=220,
    placeholder="""Paste the full job description here...

Example:
We are looking for a Data Analyst with 2+ years of experience in Python, SQL, and Excel. 
The candidate should have strong communication skills and experience with dashboards in 
Power BI or Tableau. Responsibilities include analyzing large datasets, building reports, 
and presenting insights to stakeholders..."""
)

st.markdown("### 👤 Step 3: Tell us about yourself (optional but better results)")
col1, col2 = st.columns(2)
with col1:
    experience = st.selectbox(
        "Your experience level",
        ["Fresher / 0 years", "1-2 years", "3-5 years", "5+ years"]
    )
with col2:
    your_field = st.text_input(
        "Your background/field",
        placeholder="e.g. Computer Science, Marketing, Finance"
    )

# ── Generate button ───────────────────────────────────────────────────────────
st.markdown("")
generate_btn = st.button("✨ Generate My Resume Optimizer")

# ── Generation logic ──────────────────────────────────────────────────────────
if generate_btn:
    if not api_key:
        st.error("⚠️ Please enter your Gemini API key first!")
    elif not jd_input or len(jd_input.strip()) < 50:
        st.error("⚠️ Please paste a proper job description (at least a few sentences)!")
    else:
        with st.spinner("🤖 AI is reading the job description and crafting your content..."):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-1.5-flash")

                prompt = f"""
You are an expert career coach and resume writer. A job seeker has shared a job description and needs help.

JOB DESCRIPTION:
{jd_input}

CANDIDATE INFO:
- Experience: {experience}
- Background: {your_field if your_field else "Not specified"}

Please provide the following in a clean, structured format:

===RESUME_BULLETS===
Write exactly 6 powerful, ATS-optimized resume bullet points tailored specifically to this job description.
Each bullet should:
- Start with a strong action verb
- Include metrics or numbers where possible (use realistic placeholders like [X%] if needed)
- Match the keywords and requirements from the JD
- Be relevant to the candidate's experience level
Format: Write each bullet on a new line starting with •

===COVER_LETTER_ANGLE===
Write a compelling 3-sentence cover letter opening paragraph specifically for this role.
It should mention the company's likely goals, connect to the candidate's background, and show genuine interest.
Make it feel personal, not generic.

===ATS_KEYWORDS===
List the 10 most important keywords from this JD that the candidate MUST include in their resume.
Format: keyword1, keyword2, keyword3... (comma separated on one line)

===PRO_TIP===
Give 1 specific, actionable tip for this exact job application that most candidates miss.
Keep it to 2-3 sentences max.
"""

                response = model.generate_content(prompt)
                result_text = response.text

                # ── Parse sections ─────────────────────────────────────────
                def extract_section(text, start_tag, end_tags):
                    try:
                        start = text.find(start_tag)
                        if start == -1:
                            return ""
                        start += len(start_tag)
                        end = len(text)
                        for tag in end_tags:
                            pos = text.find(tag, start)
                            if pos != -1 and pos < end:
                                end = pos
                        return text[start:end].strip()
                    except:
                        return ""

                bullets_raw   = extract_section(result_text, "===RESUME_BULLETS===",   ["===COVER_LETTER_ANGLE==="])
                cover_raw     = extract_section(result_text, "===COVER_LETTER_ANGLE===", ["===ATS_KEYWORDS==="])
                keywords_raw  = extract_section(result_text, "===ATS_KEYWORDS===",     ["===PRO_TIP==="])
                tip_raw       = extract_section(result_text, "===PRO_TIP===",           ["===END===", ""])

                st.markdown("---")
                st.markdown("## ✅ Your Personalized Results")

                # ── Resume Bullets ─────────────────────────────────────────
                st.markdown("### 📝 Resume Bullet Points")
                st.markdown("*Copy-paste these directly into your resume:*")
                if bullets_raw:
                    bullets = [b.strip() for b in bullets_raw.split("\n") if b.strip() and len(b.strip()) > 10]
                    for bullet in bullets:
                        clean = bullet.lstrip("•-* ").strip()
                        if clean:
                            st.markdown(f"""<div class="bullet-item">• {clean}</div>""", unsafe_allow_html=True)
                else:
                    st.warning("Could not parse bullets. Check your API key.")

                st.markdown("")

                # ── Cover Letter ───────────────────────────────────────────
                st.markdown("### ✉️ Cover Letter Opening")
                st.markdown("*Use this as your first paragraph:*")
                if cover_raw:
                    st.markdown(f"""<div class="cover-box">{cover_raw}</div>""", unsafe_allow_html=True)

                st.markdown("")

                # ── ATS Keywords ───────────────────────────────────────────
                st.markdown("### 🔍 ATS Keywords to Include in Your Resume")
                st.markdown("*Make sure these exact words appear in your resume:*")
                if keywords_raw:
                    keywords = [k.strip() for k in keywords_raw.replace("\n", ",").split(",") if k.strip()]
                    chips_html = "".join([f'<span class="keyword-chip">{kw}</span>' for kw in keywords])
                    st.markdown(f"""<div class="result-box">{chips_html}</div>""", unsafe_allow_html=True)

                st.markdown("")

                # ── Pro Tip ────────────────────────────────────────────────
                st.markdown("### 💡 Pro Tip for This Application")
                if tip_raw:
                    st.markdown(f"""<div class="tip-box">💡 {tip_raw}</div>""", unsafe_allow_html=True)

                # ── Download button ────────────────────────────────────────
                st.markdown("")
                st.markdown("---")
                download_content = f"""AI JOB DESCRIPTION OPTIMIZER - YOUR RESULTS
Generated by AI Prompt Optimizer Tool
============================================

RESUME BULLET POINTS:
{bullets_raw}

COVER LETTER OPENING:
{cover_raw}

ATS KEYWORDS TO INCLUDE:
{keywords_raw}

PRO TIP:
{tip_raw}
"""
                st.download_button(
                    label="📥 Download Results as Text File",
                    data=download_content,
                    file_name="job_application_optimizer.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("💡 Make sure your API key is correct. Get a free one at aistudio.google.com")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#666; font-size:12px;'>"
    "Built with Streamlit + Google Gemini AI · Free to use · "
    "Made as part of Gen AI learning journey"
    "</div>",
    unsafe_allow_html=True
)
