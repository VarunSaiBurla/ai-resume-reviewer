import fitz  # PyMuPDF
from openai import OpenAI

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def generate_resume_feedback(resume_text, api_key):
    client = OpenAI(api_key=api_key)  # ✅ use user's key

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

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert resume reviewer."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def review_resume(pdf_path, api_key):
    resume_text = extract_text_from_pdf(pdf_path)
    feedback = generate_resume_feedback(resume_text, api_key)
    return feedback
