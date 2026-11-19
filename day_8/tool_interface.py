from tool_registry import REGISTRY
from validator_decidot import decidor, validate
import time

MAX_TURNS = 5

def tool_interface(user_msg: str) -> None:
    print("="*50)
    print(f"USER: {user_msg}")
    print("-" * 50)
    tools_by_name = {t.name: t for t in REGISTRY}
    history: list[dict] = [{"role": "user", "content": user_msg}]
    for turn in range(1, MAX_TURNS + 1):
        decision = decidor(user_msg, history)
        if "content" in decision:
            print(f"TURN {turn} DECIDE: final_answer")
            print(f"MODEl: {decision['content']}")
            return
        for call in decision["tool_calls"]:
            tool = tools_by_name.get(call["name"])
            print(f"TURN {turn} DECIDE: call {call['name'] id={call['id']}}")
            print(f"   args= {json.dumps(call['arguments'])}")
            if tool is None:
                print(f"    ERROR: unknown tool {call['name']}")
                return
            errs = validate(tool.input_schema, call["arguments"])
            if errs:
                print(f"        VALIDATION ERRORS: {errs}")
                return
            if tool.consequential:
                print("     GATE: tool is consequential, would confirm")
            start = time.perf_counter()
            result = tool.executor(call['arguments'])
            ms = (time.perf_counter() - start) * 1000
            print(f"TURN {turn} EXECUTE: {tool.name} -> {json.dumps(result)} [{ms:.2f} ms]")
            history.append({
                "role": "tool", "id": call["id"], "name": tool.name, "content": json.dumps(result)
            })
        print(f"TURN {turn} OBSERVE: history length = {len(history)}")
    print("LOOP TERMINATE: hit MAX_TURNS circuit breaker")

def describe_registry() -> None:
    print("TOOL REGISTRY")
    print("-"*50)
    for t in REGISTRY:
        kind = "consequential" if t.consequential else "pure"
        print(f"    {t.name:14s} [{kind} - {t.description}]")
    print()

def main() -> None:
    print("="* 50)
    print(f"PHASE 13 LESSON 1 - THE TOOL INTERFACE")

    describe_registry()
    for query in (
            "please add 7 and 35",
            "what time is it?",
            "tell the weather in Bengaluru",
            "write me a haiku about tea",
        )
        run_loop(query)
        print()

if __name__ = "__main__":
    main()
