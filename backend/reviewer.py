import os
import time
from dotenv import load_dotenv
from google import genai
from security_scanner import scan_security_issues

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)


def format_security_findings(findings):
    if not findings:
        return "No rule-based security issues found."

    lines = []
    for item in findings:
        lines.append(
            f"- [{item['severity']}] {item['type']}: {item['description']} | Snippet: {item['snippet']}"
        )
    return "\n".join(lines)


def review_code(code: str, language: str) -> dict:
    try:
        if not api_key:
            return {"error": "GOOGLE_API_KEY not found in .env file"}

        scanner_findings = scan_security_issues(code)
        scanner_summary = format_security_findings(scanner_findings)

        prompt = f"""
You are a senior software engineer and security reviewer.

Analyze this {language} code and respond in exactly this format:

BUGS:
- (list each bug on a new line, or write "None found")

SECURITY:
- (list each security issue on a new line, or write "None found")
- Also consider these rule-based scanner findings:
{scanner_summary}

IMPROVEMENTS:
- (list each improvement suggestion, or write "None found")

SEVERITY: (write Critical / High / Medium / Low)

SCORE: (give a score out of 10)

Code to review:
{code}
"""

        last_error = None

        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                )

                return {
                    "review": response.text,
                    "language": language,
                    "scanner_findings": scanner_findings
                }

            except Exception as e:
                last_error = str(e)
                if "503" in last_error or "UNAVAILABLE" in last_error:
                    time.sleep(2)
                else:
                    break

        return {"error": last_error}

    except Exception as e:
        return {"error": str(e)}