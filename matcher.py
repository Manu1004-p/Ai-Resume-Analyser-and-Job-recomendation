import re

# -------------------------------
# ✅ TEXT PREPROCESSING
# -------------------------------

def preprocess_text(text):
    text = text.lower()
    text = text.replace("/", " ")
    text = text.replace(",", " ")
    text = text.replace("(", " ").replace(")", " ")
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    return text


# -------------------------------
# ✅ EDUCATION (UPDATED)
# -------------------------------

EDUCATION_MAP = {
    "bca": ["bca", "bachelor of computer applications"],
    "bsc_cs": ["bsc computer science", "b.sc cs"],
    "btech": ["btech", "b.e", "be", "bachelor of engineering"],
    "mca": ["mca", "master of computer applications"],

    # ✅ NON-IT EDUCATION
    "bcom": ["bcom", "bachelor of commerce"],
    "bba": ["bba", "bachelor of business administration"],
    "ba": ["ba", "bachelor of arts"],
    "mba": ["mba", "master of business administration"],
    "mcom": ["mcom", "master of commerce"],
}


def normalize_education(text):
    text = preprocess_text(text)

    for key, values in EDUCATION_MAP.items():
        for v in values:
            if v in text:
                return key
    return None


def match_education(resume_text, job_desc):
    resume_edu = normalize_education(resume_text)
    job_edu = normalize_education(job_desc)

    if job_edu is None:
        return 1

    return 1 if resume_edu == job_edu else 0


# -------------------------------
# ✅ SKILL SYNONYMS (IT + NON-IT)
# -------------------------------

SKILL_SYNONYMS = {

    # -------- IT SKILLS --------
    "python": ["python"],
    "java": ["java"],
    "javascript": ["javascript", "js"],
    "html": ["html"],
    "css": ["css"],
    "mysql": ["mysql", "database", "databases", "sql"],
    "firebase": ["firebase"],
    "flutter": ["flutter"],
    "git": ["git", "github"],
    "api": ["api", "rest api"],
    "react": ["react"],
    "nodejs": ["node", "nodejs"],

    # -------- TOOLS --------
    "excel": ["excel", "ms excel"],
    "power bi": ["power bi"],
    "tableau": ["tableau"],

    # -------- NON-IT SKILLS --------
    "communication": ["communication", "verbal communication"],
    "teamwork": ["teamwork", "team player"],
    "leadership": ["leadership", "leading team"],
    "problem solving": ["problem solving", "analytical thinking"],
    "time management": ["time management"],
    "critical thinking": ["critical thinking"],
    "decision making": ["decision making"],

    # -------- BUSINESS --------
    "marketing": ["marketing"],
    "sales": ["sales"],
    "customer service": ["customer service"],
    "finance": ["finance"],
    "accounting": ["accounting"],
    "management": ["management", "project management"],
}


# -------------------------------
# ✅ SKILL EXTRACTION
# -------------------------------

def extract_skills(text):
    text = preprocess_text(text)
    found_skills = []

    for skill, keywords in SKILL_SYNONYMS.items():
        for word in keywords:
            if re.search(r'\b' + re.escape(word) + r'\b', text):
                found_skills.append(skill)
                break

    return list(set(found_skills))


# -------------------------------
# ✅ EXPAND GENERIC TERMS
# -------------------------------

def expand_generic_skills(skills, text):
    text = text.lower()
    expanded = set(skills)

    # IT generic
    if "programming" in text:
        expanded.update(["python", "java", "javascript"])

    if "web development" in text:
        expanded.update(["html", "css", "javascript"])

    if "database" in text:
        expanded.update(["mysql"])

    # NON-IT generic
    if "communication skills" in text:
        expanded.add("communication")

    if "management skills" in text:
        expanded.add("management")

    if "analytical skills" in text:
        expanded.add("problem solving")

    return list(expanded)


# -------------------------------
# ✅ MATCHING (WEIGHTED)
# -------------------------------

IT_SKILLS = {
    "python", "java", "javascript", "html", "css",
    "mysql", "firebase", "flutter", "react", "nodejs", "api"
}


def match_skills(resume_text, job_desc):
    resume_skills = set(extract_skills(resume_text))

    job_skills = set(extract_skills(job_desc))
    job_skills = set(expand_generic_skills(job_skills, job_desc))

    if len(job_skills) == 0:
        return 0

    score = 0
    total = 0

    for skill in job_skills:

        # ✅ Weighting
        if skill in IT_SKILLS:
            weight = 1.0
        else:
            weight = 0.5

        total += weight

        if skill in resume_skills:
            score += weight

    return score / total


# -------------------------------
# ✅ FINAL SCORE
# -------------------------------

def final_score(resume_text, job_desc):
    skill_score = match_skills(resume_text, job_desc)
    edu_score = match_education(resume_text, job_desc)

    final = (0.7 * skill_score) + (0.3 * edu_score)

    return round(final * 100, 2)


# -------------------------------
# ✅ SKILL GAP
# -------------------------------

def skill_gap(resume_text, job_desc):
    resume_skills = set(extract_skills(resume_text))

    job_skills = set(extract_skills(job_desc))
    job_skills = set(expand_generic_skills(job_skills, job_desc))

    return list(job_skills - resume_skills)