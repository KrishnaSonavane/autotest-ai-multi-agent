# AutoTest AI – Log Analysis System

This project analyzes software logs to identify failures, generate bug reports, and suggest possible root causes.

Instead of relying only on AI, it combines simple rule-based checks with LLM-based reasoning to improve reliability, especially in tricky or noisy log scenarios.

---

## What it does

- Detects whether a failure occurred in logs  
- Generates a structured bug report  
- Identifies a likely root cause  
- Evaluates the output quality  

---

## Key Ideas

- Uses a **multi-step pipeline** instead of a single AI call  
- Combines **rules + LLM** to reduce false positives  
- Handles edge cases like:
  - recovered failures  
  - misleading success messages  
  - noisy logs  

---

## Tech Stack

- Python  
- LLM APIs (Groq / OpenAI)  
- JSON-based data handling  

---

## Project Structure

autotest-ai/
│
├── agents/
├── utils/
├── tests/
├── data/
├── outputs/
│
├── main.py
├── requirements.txt
├── README.md


---

##  Setup & Run
1. Install dependencies

pip install -r requirements.txt

2. Add API Key

Create a .env file:
GROQ_API_KEY=your_api_key_here

3. Run the project
python main.py --file data/sample_logs.txt

4. Run Tests
python -m tests.test_runner

5. Example Output
{
  "failure_analysis": {...},
  "bug_report": {...},
  "root_cause": {...},
  "evaluation": {...}
}

6. Results 
   1.Improved detection accuracy from ~87% to 100%
   2.Achieved 100% Precision, Recall, and F1 Score on custom test cases
   3.Successfully handled multiple real-world edge cases

## Notes

This is a learning project focused on building a reliable pipeline.  
In real-world systems, performance may vary depending on log complexity.

---

## Author

Krishna Sonavane

