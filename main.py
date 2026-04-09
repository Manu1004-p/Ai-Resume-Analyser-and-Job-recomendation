from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename

from resume_parser import extract_text
from matcher import analyze_resume   # ✅ UPDATED IMPORT
from job_matcher import fetch_jobs_from_resume

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# -------------------------------
# ✅ ROUTES
# -------------------------------

@app.route("/")
def welcome():
    return render_template("welcome.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# -------------------------------
# ✅ ANALYZE RESUME
# -------------------------------

@app.route("/analyze", methods=["GET", "POST"])
def analyze():

    if request.method == "POST":

        file = request.files.get("resume")

        if not file or file.filename == "":
            return "No file uploaded"

        job_description = request.form.get("job_description", "")

        # Save file
        filename = secure_filename(file.filename)
        path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(path)

        # Extract text
        resume_text = extract_text(path)

        # ✅ MAIN ANALYSIS (ONE FUNCTION)
        result = analyze_resume(resume_text, job_description)

        return render_template("result.html", result=result)

    return render_template("index.html")


# -------------------------------
# ✅ JOB FETCH
# -------------------------------

@app.route("/jobs", methods=["GET", "POST"])
def jobs():

    jobs_list = []
    detected_skills = []

    if request.method == "POST":

        file = request.files.get("resume")

        if file and file.filename != "":
            filename = secure_filename(file.filename)
            path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(path)

            resume_text = extract_text(path)

            jobs_list, detected_skills = fetch_jobs_from_resume(resume_text)

    return render_template("jobs.html", jobs=jobs_list, skills=detected_skills)


# -------------------------------
# ✅ RUN APP
# -------------------------------

if __name__ == "__main__":
    app.run(debug=True)