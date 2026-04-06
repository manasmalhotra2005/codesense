import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def review_code(code: str, language: str) -> dict:
    prompt = f"""
You are a senior software engineer doing a professional code review.
Analyze this {language} code and respond in exactly this format:

BUGS:
- (list each bug on a new line, or write "None found")

SECURITY:
- (list each security issue, or write "None found")

IMPROVEMENTS:
- (list each improvement suggestion, or write "None found")

SEVERITY: (write Critical / High / Medium / Low)

SCORE: (give a score out of 10)

Code to review:
{code}
"""
    response = model.generate_content(prompt)
    return {
        "review": response.text,
        "language": language
    }