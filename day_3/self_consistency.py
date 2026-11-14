from cot_prompt_builder import build_cot_prompt
from testing_harness import format_openrouter_request, llm_call

def extract_answer(text):
    if not text:
        return None
    patterns = [
        r"[Tt]he answer is[:\s]*\$?([\d,]+\.?\d*)",
        r"[Tt]he answer is[:\s]*([\d,]+\.?\d*)",
        r"#### ([\d,]+\.?\d*)",
        r"= \$?([\d,]+\.?\d*)\s*$",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1).replace(",", "")
    numbers = re.findall(r"[\d,]+\.?\d*", text)
    if numbers:
        return numbers[-1].replace(",", "")
    return None

class Counter:
    """A simple labelled counter."""

    name: str
    help: str = ""
    values: dict[tuple[tuple[str, str], ...], float] = field(default_factory=dict)

    def inc(self, labels: dict[str, str] | None = None, by: float = 1.0) -> None:
        key = _label_key(labels or {})
        self.values[key] = self.values.get(key, 0.0) + by

    def get(self, labels: dict[str, str] | None = None) -> float:
        return self.values.get(_label_key(labels or {}), 0.0)

def self_consistency_solve(question, examples, client, model, n_samples=5):
    system, user = build_cot_prompt(question, examples)

    answers = []
    reasonings = []

    for _ in range(n_samples):
        message = format_openrouter_request(
            {"system": system, "user": user}, 
            model
        )
        response = llm_call(message)
        text = response["response"]
        reasonings.append(text)
        answer =  extract_answer(text)
        if answer is not None:
            answers.append(answer)

        vote_counts = Counter(answers)
        best_answer = vote_countes.most_common(1)[0][0] if vote_counts else None
        confidence = vote_counts[best_answer] / len(answers) if best_answer else 0.0

        return best_answer, confidence, reasonings, vote_counts
