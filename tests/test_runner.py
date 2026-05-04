import json
from agents.failure_analyzer import analyze_failure

def run_tests():
    with open("data/test_cases.json", "r") as f:
        test_cases = json.load(f)

    TP = TN = FP = FN = 0

    print("\nRunning Test Cases...\n")

    for test in test_cases:
        result = analyze_failure(test["log"])
        predicted = result["failure_detected"]
        expected = test["expected_failure"]

        if predicted and expected:
            TP += 1
        elif not predicted and not expected:
            TN += 1
        elif predicted and not expected:
            FP += 1
        elif not predicted and expected:
            FN += 1

        print(f"Test: {test['name']}")
        print(f"Expected: {expected}, Predicted: {predicted}")
        print(f"Result: {'PASS' if predicted == expected else 'FAIL'}\n")

    total = TP + TN + FP + FN
    accuracy = (TP + TN) / total

    precision = TP / (TP + FP) if (TP + FP) else 0
    recall = TP / (TP + FN) if (TP + FN) else 0
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) else 0

    print("=" * 40)
    print(f"Accuracy : {accuracy:.2f}")
    print(f"Precision: {precision:.2f}")
    print(f"Recall   : {recall:.2f}")
    print(f"F1 Score : {f1:.2f}")
    print("=" * 40)

    print("\nConfusion Matrix:")
    print(f"TP: {TP}, FP: {FP}")
    print(f"FN: {FN}, TN: {TN}")


if __name__ == "__main__":
    run_tests()