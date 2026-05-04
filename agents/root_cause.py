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


def analyze_root_cause(failure_data: dict, bug_report: dict) -> dict:
    log_info("Starting Root Cause Analysis")
    system_prompt = """
You are an expert debugging engineer.

Rules:
- Return ONLY valid JSON
- No explanations
- No markdown
- Be specific and practical
"""

    user_prompt = f"""
Analyze the failure and identify root cause.

Failure Data:
{failure_data}

Bug Report:
{bug_report}

Output JSON ONLY:
{{
  "root_cause": "",
  "confidence": 0.0,
  "suggested_fix": ""
}}
"""

    response = call_llm(system_prompt, user_prompt)

    log_info(f"LLM Response (Root Cause): {response}")

    try:
        clean_json = extract_json(response)
        return json.loads(clean_json)
    
        log_info(f"Parsed Result (Root Cause): {result}")

        return result
    
    except Exception as e:
        log_error(f"Parsing failed in Root Cause: {str(e)}")

        return {
            "root_cause": "Unknown",
            "confidence": 0.0,
            "suggested_fix": "Parsing failed",
        }