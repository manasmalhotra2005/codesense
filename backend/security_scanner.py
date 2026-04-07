import re


def scan_security_issues(code: str):
    findings = []

    patterns = [
        {
            "name": "Hardcoded Password",
            "pattern": r'(?i)(password|passwd|pwd)\s*=\s*["\'][^"\']+["\']',
            "severity": "Critical",
            "description": "Possible hardcoded password found in source code."
        },
        {
            "name": "Hardcoded API Key",
            "pattern": r'(?i)(api_key|apikey|secret_key|token)\s*=\s*["\'][^"\']+["\']',
            "severity": "High",
            "description": "Possible hardcoded API key or secret token found."
        },
        {
            "name": "Use of eval()",
            "pattern": r'\beval\s*\(',
            "severity": "High",
            "description": "Use of eval() can execute arbitrary code and is dangerous."
        },
        {
            "name": "Use of exec()",
            "pattern": r'\bexec\s*\(',
            "severity": "High",
            "description": "Use of exec() can execute arbitrary code dynamically."
        },
        {
            "name": "Use of os.system()",
            "pattern": r'\bos\.system\s*\(',
            "severity": "High",
            "description": "os.system() may lead to command injection if inputs are not sanitized."
        },
        {
            "name": "Risky subprocess usage",
            "pattern": r'\bsubprocess\.(Popen|call|run)\s*\(',
            "severity": "Medium",
            "description": "Subprocess execution should be reviewed for command injection risks."
        },
        {
            "name": "Possible SQL Injection",
            "pattern": r'(?i)(SELECT|INSERT|UPDATE|DELETE).*(\+|%s|f["\'])',
            "severity": "High",
            "description": "Possible SQL query string construction detected. Use parameterized queries."
        },
    ]

    for rule in patterns:
        matches = re.finditer(rule["pattern"], code)
        for match in matches:
            findings.append({
                "type": rule["name"],
                "severity": rule["severity"],
                "description": rule["description"],
                "snippet": match.group(0)
            })

    return findings