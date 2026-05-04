from utils.llm_client import call_llm
from utils.logger import log_info, log_error
import json
import re

def extract_json(text: str) -> str:
    match = re.search(r"```json(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return match.group(0)

    return text


def generate_bug_report(failure_data: dict) -> dict:
    system_prompt = """
You are a senior QA engineer.

Rules:
- Return ONLY valid JSON
- No explanations
- No markdown
- Keep answers concise
"""

    user_prompt = f"""
Convert this failure data into a professional bug report:

{failure_data}

Output JSON ONLY:
{{
  "title": "",
  "description": "",
  "severity": "Low/Medium/High/Critical",
  "steps_to_reproduce": "",
  "expected_behavior": "",
  "actual_behavior": ""
}}
"""

    response = call_llm(system_prompt, user_prompt)

    log_info(f"LLM Response (Bug Reporter): {response}")

    try:
        clean_json = extract_json(response)
        return json.loads(clean_json)
        
        log_info(f"Parsed Result (Bug Reporter): {result}")

        return result
        
    except Exception as e:
        log_error(f"Parsing failed in Bug Reporter: {str(e)}")

        return {
            "title": "Parsing Failed",
            "description": response,
            "severity": "Unknown",
            "steps_to_reproduce": "",
            "expected_behavior": "",
            "actual_behavior": ""
        }