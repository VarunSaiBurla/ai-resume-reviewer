from openai import OpenAI
import fitz

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def review_resume(pdf_path, api_key):
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

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert resume reviewer."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

def score_resume(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    if len(text) < 500:
        return 40
    elif len(text) < 1000:
        return 65
    else:
        return 85

def extract_missing_sections(pdf_path):
    text = extract_text_from_pdf(pdf_path).lower()
    sections = ["summary", "experience", "education", "skills", "projects"]
    missing = [s.capitalize() for s in sections if s not in text]
    return missing
