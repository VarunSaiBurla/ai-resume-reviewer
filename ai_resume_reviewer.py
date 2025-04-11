import openai
import os
import fitz  # PyMuPDF
import argparse

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def generate_resume_feedback(resume_text):
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

def review_resume(pdf_path):
    resume_text = extract_text_from_pdf(pdf_path)
    feedback = generate_resume_feedback(resume_text)
    return feedback

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Resume Reviewer")
    parser.add_argument("--file", required=True, help="Path to resume PDF")
    args = parser.parse_args()

    result = review_resume(args.file)
    print("\n===== AI Feedback =====\n")
    print(result)
