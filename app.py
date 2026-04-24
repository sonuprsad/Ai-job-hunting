import streamlit as st
from auth.auth import login, register
from scraper.linkedin import get_jobs
from matcher.ai_matcher import ai_match_score
from matcher.insights import get_insights
from PyPDF2 import PdfReader

st.set_page_config(page_title="AI Job Agent", layout="wide")

# ---------------- SESSION INIT ----------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# ---------------- LOGIN / REGISTER ----------------
if not st.session_state["logged_in"]:

    st.title("🔐 AI Job Agent")

    menu = st.radio("Choose Option", ["Login", "Register"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["Candidate", "HR"])

    # -------- REGISTER --------
    if menu == "Register":
        if st.button("Register"):
            success, msg = register(username, password, role)
            if success:
                st.success("✅ Registered Successfully! Now login.")
            else:
                st.error(msg)

    # -------- LOGIN --------
    elif menu == "Login":
        if st.button("Login"):
            success, msg, user_role = login(username, password)
            if success:
                st.session_state["logged_in"] = True
                st.session_state["role"] = user_role
                st.session_state["username"] = username
                st.success("✅ Login Successful")
                st.rerun()
            else:
                st.error(msg)

    st.stop()

# ---------------- TOP BAR ----------------
col1, col2 = st.columns([6, 1])

with col1:
    st.write(f"👤 Welcome {st.session_state['username']} ({st.session_state['role']})")

with col2:
    if st.button("🔓 Logout"):
        st.session_state.clear()
        st.success("Logged out successfully")
        st.rerun()

# ---------------- DASHBOARD ----------------
st.title("🚀 AI Job Dashboard")

# =========================
# 👤 CANDIDATE DASHBOARD
# =========================
if st.session_state["role"] == "Candidate":

    st.subheader("📄 Upload / Paste Resume")

    uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "txt"])
    resume_text = ""

    if uploaded_file:
        if uploaded_file.type == "application/pdf":
            reader = PdfReader(uploaded_file)
            for page in reader.pages:
                resume_text += page.extract_text()
        else:
            resume_text = uploaded_file.read().decode("utf-8")

    resume_input = st.text_area("OR Paste Resume")

    resume = resume_text if resume_text else resume_input

    if st.button("🚀 Analyze Resume"):

        if not resume:
            st.warning("Please upload or paste resume")
            st.stop()

        jobs = get_jobs()
        results = []

        for job in jobs:
            score = ai_match_score(resume, job["desc"])
            insights = get_insights(resume, job["desc"])

            results.append((job["title"], score, insights, job["desc"]))

        results.sort(key=lambda x: x[1], reverse=True)

        st.subheader("🔥 Top Job Matches")

        for title, score, insights, desc in results[:5]:

            with st.container():
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.write(f"### {title}")
                    st.write(desc[:200] + "...")

                with col2:
                    if score > 70:
                        st.success(f"{score}%")
                    elif score > 40:
                        st.warning(f"{score}%")
                    else:
                        st.error(f"{score}%")

                st.write("✅ Matched Skills:", ", ".join(insights["matched"]))
                st.write("❌ Missing Skills:", ", ".join(insights["missing"]))

                st.divider()

        # -------- OVERALL SCORE --------
        avg_score = sum([r[1] for r in results[:5]]) / 5

        st.subheader("📊 Overall Resume Score")
        st.progress(int(avg_score))
        st.write(f"Score: {round(avg_score,2)}%")

        # -------- FEEDBACK --------
        if avg_score > 70:
            st.success("🔥 Strong Resume — Apply confidently")
        elif avg_score > 50:
            st.warning("⚠️ Improve your resume")
        else:
            st.error("❌ Weak Resume — Needs major improvement")

        # -------- SUGGESTIONS --------
        st.subheader("📌 Suggestions")

        if "project" not in resume.lower():
            st.write("👉 Add real-world projects")

        if "react" not in resume.lower():
            st.write("👉 Add frontend (React) skills")

        if "django" not in resume.lower():
            st.write("👉 Add backend frameworks")

        if "docker" not in resume.lower():
            st.write("👉 Add DevOps tools (Docker/AWS)")

# =========================
# 🧑‍💼 HR DASHBOARD
# =========================
elif st.session_state["role"] == "HR":

    st.subheader("🧑‍💼 HR Dashboard")

    job_desc = st.text_area("📄 Paste Job Description")
    candidate_resume = st.text_area("📄 Paste Candidate Resume")

    if st.button("🔍 Analyze Candidate"):

        if not job_desc or not candidate_resume:
            st.warning("Please fill both fields")
            st.stop()

        score = ai_match_score(candidate_resume, job_desc)
        insights = get_insights(candidate_resume, job_desc)

        st.subheader("📊 Candidate Match Result")

        if score > 70:
            st.success(f"🔥 Strong Candidate → {score}%")
        elif score > 40:
            st.warning(f"⚠️ Average Candidate → {score}%")
        else:
            st.error(f"❌ Weak Candidate → {score}%")

        st.write("✅ Matched Skills:", ", ".join(insights["matched"]))
        st.write("❌ Missing Skills:", ", ".join(insights["missing"]))