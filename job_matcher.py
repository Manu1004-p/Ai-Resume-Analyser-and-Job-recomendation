import requests

APP_ID = "d4a3d41c"
APP_KEY = "37368d54e6eb05a746645e4a2ff72d86"

def fetch_jobs_from_resume(resume_text):

    common_skills = [
        "python","java","c++","html","css","javascript",
        "react","node","sql","machine learning",
        "data science","excel","accounting","marketing",
        "sales","management","nursing","teaching",
        "finance","banking","mechanical","civil"
    ]

    detected_skills = []

    for skill in common_skills:
        if skill in resume_text:
            detected_skills.append(skill)

    query = " ".join(detected_skills[:5]) if detected_skills else "jobs"

    url = "https://api.adzuna.com/v1/api/jobs/in/search/1"

    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "results_per_page": 10,
        "what": query
    }

    response = requests.get(url, params=params)
    data = response.json()

    jobs = []

    for job in data.get("results", []):
        jobs.append({
            "title": job.get("title"),
            "company": job.get("company", {}).get("display_name"),
            "location": job.get("location", {}).get("display_name"),
            "link": job.get("redirect_url")
        })

    return jobs, detected_skills

