import openai
import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def review_resume(pdf_path, api_key):
    openai.api_key = api_key
    resume_text = extract_text_from_pdf(pdf_path)
    prompt = f"""
    You are a professional resume reviewer. Analyze the following resume text and provide structured feedback:

    1. Formatting: Comments on layout, readability, and section structure.
    2. Clarity: Whether the responsibilities and achievements are clear.
    3. Grammar & Style: Spelling, grammar, sentence structure.
    4. Impact: Suggestions to make it more results-oriented and impactful.

    Resume:
    ---
    {resume_text}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert resume reviewer."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def score_resume(pdf_path):
    resume_text = extract_text_from_pdf(pdf_path)
    score = len(resume_text.split())  # Just a mock scoring logic
    score = min(100, max(30, score // 10))
    return score

def extract_missing_sections(pdf_path):
    resume_text = extract_text_from_pdf(pdf_path).lower()
    sections = ["summary", "education", "experience", "skills", "projects", "certifications"]
    missing = [section.title() for section in sections if section not in resume_text]
    return missing
