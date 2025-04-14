import fitz  # PyMuPDF
from openai import OpenAI


def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def review_resume(pdf_path, api_key):
    client = OpenAI(api_key=api_key)
    resume_text = extract_text_from_pdf(pdf_path)

    prompt = f"""
    You are a professional resume reviewer. Analyze the following resume and give structured feedback:

    1. Formatting: layout, readability, section clarity.
    2. Clarity: Are achievements and responsibilities clearly stated?
    3. Grammar & Style: spelling, grammar, sentence structure.
    4. Impact: How results-oriented and impressive is it?
    5. Suggestions: What could be improved?

    Resume:
    ---
    {resume_text}
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert resume reviewer."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()


def score_resume(pdf_path):
    resume_text = extract_text_from_pdf(pdf_path)
    score = 50

    if "experience" in resume_text.lower():
        score += 10
    if "education" in resume_text.lower():
        score += 10
    if "skills" in resume_text.lower():
        score += 10
    if "projects" in resume_text.lower():
        score += 10
    if len(resume_text) > 500:
        score += 10

    return min(score, 100)


def extract_missing_sections(pdf_path):
    resume_text = extract_text_from_pdf(pdf_path).lower()
    expected_sections = ["experience", "education", "skills", "projects", "certifications", "summary"]
    missing = [section.capitalize() for section in expected_sections if section not in resume_text]
    return missing
