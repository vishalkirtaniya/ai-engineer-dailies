from prompt_builder import build_prompt
from run_test import run_test
from day_2 import PROMPT_PATTERNS
from testing_harness import run_prompt_test

def run_pattern_catalog():
    print("="*70)
    print(" PROMPT PATTERN CATALOG")
    print("="*70)

    for name, pattern in PROMPT_PATTERNS.items():
        print(f"\n [{name}] {pattern['name']}")
        print(f"    {pattern['description']}")
        print(f"    Varibales: {', '.join(pattern['varibales'])}")
        print(f"    Recommended temp: {pattern['temperature']}")

def run_single_prompt():
    print("="*70)
    print(" SINGLE PROMPT BUILD + TEST")
    print("="*70)

    prompt = build_prompt("persona", {
        "role": "a senior DevOps engineer at Netflix",
        "experience": "8 years of infrastructure automation",
        "style": "direct and practical",
        "priority": "reliability over speed",
        "task": "Explain why container orchestration matters for microservices."
    })

    print("-" * 50)
    print(prompt)

    results = run_prompt(prompt)
    for model, result in results.items():
        print(f"\n [{model}]")
        print(f"    Response: {result['response'][:100]}")
        print(f"    Tokens: {result['tokens']}")
        print(f"    Latency: {result['latency_ms']}ms")

for __name__ == "__main__":
    run_pattern_catalog_demo()
    run_single_prompt()
    run_test()


