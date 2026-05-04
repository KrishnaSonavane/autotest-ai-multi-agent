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


def analyze_failure(log_text: str) -> dict:
    log_info("Starting Failure Analysis")

    # 🔥 ===== PRE-CHECK (RUN BEFORE LLM) =====
    log_lower = log_text.lower()
    log_lower = " ".join(log_lower.split())

    # 🔥 CASE 1: Historical resolved → NOT failure
    if (
        "previous" in log_lower
        and "resolved" in log_lower
        and any(x in log_lower for x in ["successfully", "running normally", "completed"])
    ):
        log_info("Detected historical resolved log → NO failure")

        return {
            "failure_detected": False,
            "failure_type": "",
            "error_message": "",
            "observations": "Historical issue resolved"
        }

    # 🔥 CASE 2: Active failure + recovery → STILL failure
    if (
        any(x in log_lower for x in ["failure", "failed", "exception", "timeout"])
        and any(x in log_lower for x in ["recovered", "recovery", "resolved"])
        and "previous" not in log_lower
    ):
        log_info("Detected failure followed by recovery → STILL failure")

        return {
            "failure_detected": True,
            "failure_type": "Recovered Failure",
            "error_message": "Failure occurred but system recovered",
            "observations": "Active failure followed by recovery"
        }

    # ===== LLM PROMPTS =====
    system_prompt = """
You are a strict software log analyzer.

Rules:
- Return ONLY valid JSON. No explanations.
- A FAILURE means ANY of the following appears anywhere in the logs:
  - exception, error, failed, failure, timeout, non-zero exit code
- If BOTH success and failure signals appear, FAILURE takes priority.
- Warnings alone are NOT failures.
"""

    user_prompt = f"""
Analyze the logs carefully.

Important:
- Detect ACTUAL failures only.
- Ignore historical or already resolved issues.

Logs:
{log_text}

Return ONLY JSON:
{{
  "failure_detected": true/false,
  "failure_type": "",
  "error_message": "",
  "observations": ""
}}
"""

    response = call_llm(system_prompt, user_prompt)

    log_info(f"LLM Response (Failure Analyzer): {response}")

    try:
        clean_json = extract_json(response)
        result = json.loads(clean_json)

        log_info(f"Parsed Result (Failure Analyzer): {result}")

        return result

    except Exception as e:
        log_error(f"Parsing failed in Failure Analyzer: {str(e)}")

        return {
            "failure_detected": False,
            "failure_type": "unknown",
            "error_message": f"Parsing failed: {str(e)}",
            "observations": response
        }