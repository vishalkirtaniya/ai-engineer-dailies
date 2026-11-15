from cot_prompt_builder import few_shot_cot_solve
from self_consistency import self_consistency_solve
from tot_solver import tree_of_thought_solve

def solve_with_escalation(question, examples, model):
    single_answer, _ = few_shot_cot_solve(question, example, model)

    sc_answer, confidence, _, _ = self_consistency_solve(
        question, examples, model, n_samples=5
    )

    if confidence >= 0.8 and single_answer == sc_answer:
        return sc_answer, "self_consistency", confidence

    tot_answer, _ = tree_of_thought_solve(question, model)
    return tot_answer, "tree_of_thought", None
