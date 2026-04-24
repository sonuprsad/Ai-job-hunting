def get_insights(resume, job_desc):
    resume_words = set(resume.lower().split())
    job_words = set(job_desc.lower().split())

    return {
        "matched": list(resume_words & job_words),
        "missing": list(job_words - resume_words)
    }