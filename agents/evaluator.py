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


def evaluate_output(failure_data: dict, bug_report: dict, root_cause: dict) -> dict:
    log_info("Starting Evaluation")
    system_prompt = """
You are a strict and logical software evaluator.

Rules:
- Return ONLY valid JSON
- No explanations outside JSON
- Scores must match feedback
- Be consistent and objective
"""

    user_prompt = f"""
Evaluate the outputs based on:

Criteria:
- Correctness (is it accurate?)
- Completeness (all fields meaningful?)
- Clarity (clear and understandable?)

Failure Analysis:
{failure_data}

Bug Report:
{bug_report}

Root Cause Analysis:
{root_cause}

Scoring Guide:
- 9–10: Excellent
- 7–8: Good
- 5–6: Average
- 1–4: Poor

Output JSON ONLY:
{{
  "failure_analysis_score": 0,
  "bug_report_score": 0,
  "root_cause_score": 0,
  "overall_score": 0,
  "feedback": ""
}}
"""

    response = call_llm(system_prompt, user_prompt)

    log_info(f"LLM Response (Evaluator): {response}")

    try:
        clean_json = extract_json(response)
        return json.loads(clean_json)
    
        log_info(f"Parsed Result (Evaluator): {result}")  

        return result  

    except Exception as e:
        
        log_error(f"Parsing failed in Evaluator: {str(e)}")
        return {
            "failure_analysis_score": 0,
            "bug_report_score": 0,
            "root_cause_score": 0,
            "overall_score": 0,
            "feedback": response
        }