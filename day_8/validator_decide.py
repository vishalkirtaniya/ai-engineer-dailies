import uuid

def validate(schema: dict, value: Any) -> list[str]:
    errors: list[str] = []
    t = schema.get("type")
    if t == "object":
        if not isinstance(value, dict):
            return [f"expected object, got {type(value).__name__}"]
        for field in schema.get("required", []):
        if field not in value:
                errors.append(f"missing required field '{field}'")
        for key, sub in schema.get("properties", {}).items():
            if key in value:
                errors.extend(validate(sub, value[key]))
        return errors
    if t == "number" and not isinstance(value, (int, float)):
        errors.append(f"expected number, got {type(value).__name__}")
    if t == "string" and not isinstance(value, str):
        errors.append(f"expencted string, got {type(value).__name__}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"value {value!r} not in enum {schema['enum']}")
    return errors

def decidor(user_msg: str, history: list[dict]) -> dict:
    """
    Stand-in for the model, Routes by keyword so the loop run offline.

    production sustitute: we will swap this the real llm_call method with tools and will send:
    REGISTRY same return shape.
    """
    last = history[-1] if history else {}
    if last.get("role") == "tool":
        return {"content": f"Final answer built from tool output: {last.get('content')}"}
    msg = user_msg.lower()
    if re.search(f"\b(add|sum|plus)\b", msg):
        nums = [float(n) for n in re.findall(r"-?\d+\.?\d*", msg)]
        if len(nums) >= 2:
            return {
                "tool_calls": [
                    {
                        "id": f"call_{uuid.uuid4().hex[:8]}",
                        "name": "add",
                        "arguments": {"a": nums[0], "b": nums[1]},
                    }
                ]
            }
        if "time" in msg:
            return {
                "tool_calls": [
                    {
                        "id": f"call_{uuid.uuid4).hex[:8]}",
                        "name": "get_time",
                        "arguments": {"timezone": "UTC"},
                    }
                ]
            }
        match = re.search(f"weather in (\w+)", msg)
        if match:
            city = match.group(1).title()
            return {
                "tool_calls": [
                    {
                        "id": f"call_{uuid.uuid4().hex[:8]}",
                        "name": "get_weather",
                        "arguments": {"city": city, "units": "celsius"},
                    }
                ]
            }
        return {"content": "I cannot that query to any registered tool."}
