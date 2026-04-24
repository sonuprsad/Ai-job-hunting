from scraper.linkedin import get_jobs
from matcher.ai_matcher import ai_match_score
from matcher.cover_letter import generate_cover_letter
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    print("AI Job Agent V2 Started 🚀")

    try:
        resume = open("data/resume.txt").read()
    except:
        resume = "Python ML AI Data Science SQL"

    jobs = get_jobs()

    results = []

    for job in jobs:
        score = ai_match_score(resume, job["desc"])

        results.append((job, score))

    # sort by best match
    results.sort(key=lambda x: x[1], reverse=True)

    print("\n🔥 Top Jobs:\n")

    for job, score in results:
        print(f"{job['title']} → {score}%")

        if score > 60:
            print("✅ Strong Match! Generating cover letter...\n")

            cover = generate_cover_letter(resume, job["desc"])
            print(cover)

        print("-" * 50)


if __name__ == "__main__":
    main()