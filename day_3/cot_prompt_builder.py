def build_cot_prompt(question, examples, num_examples=3):
    system = (
        "You are a math problem solver. \n"
        "For each problem, show your step-by-step reasoning. \n"
        "then give the final numerical answer on the last line. \n"
        "in the format: 'The answer is [number]'"
    )
    
    example_text = ""
    for ex in examples[:num_examples]:
        example_text += f"Q: {ex['question']} \n"
        example_text += f"A: {ex['reasoning']} The answer is {ex['answer']}. \n\n"

    user = f"{example_text}Q: {ex['question']}\nA:"
    return system, user
