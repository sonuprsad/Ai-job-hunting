import re

IMPORTANT_SKILLS = {
    "python": 2, "machine": 2, "learning": 2, "sql": 2,
    "react": 2, "node": 2, "mongodb": 2,
    "django": 2, "flask": 2, "api": 2
}

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    return text.split()

def ai_match_score(resume, job_desc):
    resume_words = clean_text(resume)
    job_words = clean_text(job_desc)

    if not resume_words or not job_words:
        return 0

    score = 0
    max_score = 0

    for word in job_words:
        weight = IMPORTANT_SKILLS.get(word, 1)
        max_score += weight

        if word in resume_words:
            score += weight

    return round((score / max_score) * 100, 2)