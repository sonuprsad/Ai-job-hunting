import requests
from bs4 import BeautifulSoup

def get_static_jobs():
    return [
        {"title": "Data Scientist", "desc": "Python Machine Learning SQL AI Statistics Pandas"},
        {"title": "Backend Developer", "desc": "Python Django Flask API SQL Backend"},
        {"title": "MERN Developer", "desc": "React Node MongoDB Express JavaScript"},
    ]

def get_real_jobs():
    jobs = []

    try:
        url = "https://remoteok.com/remote-dev-jobs"
        headers = {"User-Agent": "Mozilla/5.0"}

        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        job_rows = soup.find_all("tr", class_="job")

        for job in job_rows[:15]:
            try:
                title = job.find("h2").text.strip()
                desc = job.get_text(" ").strip()

                jobs.append({"title": title, "desc": desc})
            except:
                continue

    except:
        return get_static_jobs()

    return jobs if jobs else get_static_jobs()

def get_jobs():
    return get_real_jobs()