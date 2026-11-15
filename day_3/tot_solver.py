from testing_harness import format_openrouter_request, llm_call

def generate_initial_thoughts(question, model, breadth=3):
    system = (
        "You are a math problem solver exploring different solution approaches.\n"
        "Generate one distinct approach to solving this problem. \n"
        "Show your partial reasoning. Do not give the final answer yet."
    )
    thoughts = []
    for i in range(breadth):
        user = (
            f"Problem: {question}\n\n"
            f"Generate approach #{i+1} (use a different strategy than previous approaches) (use a different strategy than previous approaches). \n"
            f"Think about: arithmetic breakdown, working backwards, estimation, \n"
            f"or algebraic formulation."
        )
        prompt = {"system": system, "user": user}
        message = format_openrouter_request(prompt, model)
        text = llm_call(message)
        thoughts.append(text)
    return thoughts

def evaluate_thought(thought, question, model):
    system = (
        "You are a math reasoning evaluator. \n"
        "Score the following partial reasoniing on a scale from 0.0 to 1.0. \n"
        "Consider: correctness of arithmetic, logical coherence, \n"
        "progress toward the answer. \n"
        "Respond with ONLY a number between 0.0 to 1.0."
    )
    user = f"Problem: {question}\n\nReasoning so far:\n{thought}\n\nScore:"
    prompt = {"system": system, "user": user}
    text = llm_call(prompt, model)
    try:
        score = float(re.search(r"([\d.]+)", text).group(1))
        return min(max(score, 0.0), 1.0)
    except (AttributeError, ValueError):
        return 0.5

def extend_thought(thought, question, model, breadth=2):
    system = (
        "You are a math problem solver continuining a line of reasoning. \n"
        "Take the partial reasoning below and extend if further toward a solution. \n"
        "Show your continued reasoning. If you reach the final answer. \n"
        "state it as: 'the answer is [number]'."
    )
    extensions = []
    for i in range(breadth):
        user = (
            f"Problem: {question}\n\n"
            f"Reasoning so far: \n{thought}\n\n"
            f"Continue this reasoning (approach #{i+1}):"
        )
        prompt = {"system": system, "user": user, "temperature": 0.8}
        text = llm_call(prompt, model)
        extensions.append(f"{thought}\n\n{text}")
    return extensions

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

def tree_of_thought_solve(question, model, breadth=3, depth=3):
    thoughts = generate_initial_thoughts(question, model, breadth)
    scored = [(t, evaluate_thought(t, question, model)) for t in thoughts]
    scored.sort(key=lambda x: x[1], reverse=True)

    for current_depth in range(1, depth):
        next_thoughts = []
        top_k = min(2, len(scored))
        for thought, score in scored[:top_k]:
            extensions = extend_thought(thought, question, model, breadth)
            for ext in extensions:
                ext_score = evaluate_thought(ext, question, model)
                next_thoughts.append(ext, ext_score)
        if next_thoughts:
            scored = sorted(next_thoughts, key=lambda x: x[1], reverse=True)

    best_thought = score[0][0] if scored else ""
    return extract_answer(best_thought), best_thought
