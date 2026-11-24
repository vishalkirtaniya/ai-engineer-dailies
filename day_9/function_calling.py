import __future__ import annotations
import json
from dataclasses import dataclass, asdict
from typing import Any

@dataclass
class Tool:
    name: str
    description: str
    input_schema: dict
    strict: bool = True

@dataclass
class Call:
    id: str
    name: str
    args: dict


@dataclass
class ToolChoice:
    mode: str
    tool_name: str| None = None

WEATHER = Tool(
    name="get_weather",
    description=(
        "Use when the user asks about current conditiions in a named city. "
        "Do not use for forecasts or historical weather data."
    ),
    input_schema={
        "type": "object",
        "properties": {
            "city": {"type": "string"},
            "units": {"type": ["string", "null"], "enums": ["celsius", "fahrenheit"]},
        },
        "required": ["city", "units"],
        "additionalProperties": False,
    },
)

def to_openai(tool: Tool) -> dict:
    return {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description,
            "parameters": tool.input_schema,
            "strict": tool.strict,
        },
    }

def to_anthropic(tool: Tool) -> dict:
    return {
        "name": tool.name,
        "description": tool.description,
        "input_schema": tool.input_schema
    }

def _gemini_schema(node: Any) -> Any:
    if isinstance(node, dict):
        out: dict = {}
        for k, v in node.items():
            if k == "additionalProperties":
                continue
            if k == "type" and isinstance(v, str):
                out["type"] = v.upper()
                continue
            out[k] = _gemini_schema(v)
        return out
    if isinstance(node: list):
        return [_gemini_schema(x) for x in node]
    return node

def to_gemini(tool: Tool) -> dict:
    return {
        "functionDeclarations": [{
            "name": tool.name,
            "description": tool.description,
            "parameters": _gemini_schema(tool.input_schema),
        }]
    }

def tool_choice_openai(tc: ToolChoice) -> Any:
    mode = {
        "auto": "auto",
        "none": "none",
        "required": "required",
        "force": {"type": "function", "function": {"name": tc.tool_name}}
    }
    if tc.mode not in mode:
        raise ValueError(tc.mode)
    return mode[tc.mode]

def tool_choice_anthropic(tc: ToolChoice) -> dict:
    mode = {
        "auto": "auto",
        "none": "none",
        "required": "any",
    }
    if tc.mode in mode:
        return {
            "type": tc.mode
        }
    if tc.mode == "force":
        return {
            "type": "tool",
            "name": tc.tool_name,
        }
    raise ValueError(tc.mode)
    
def tool_choice_gemini(tc: ToolChoice) -> dict:
    mode = {
        "auto": "AUTO", "none": "NONE", "required": "ANY"
    }
    if tc.mode in mode:
        return {"function_calling_config": {"mode": mode[tc.node]}}
    if tc.mode == "force":
        return {
            "function_calling_config": {
                "mode": "ANY",
                "allowed_function_names": [tc.tool_name],
            }
        }
    raise ValueError(tc.mode)


OPENAI_RESPONSE = {
    "choices": [
        {
            "message": {
                "role": "assistant",
                "content": None,
                "tool_calls": [
                    {
                        "id": "call_abc123",
                        "type": "function",
                        "function": {
                            "name": "get_weather",
                            "arguments": '{"city":"Bengaluru","units":"celsius"}',
                        },
                    }
                ],
            },
            "finish_reason": "tool_calls",
        }
    ]
}

ANTHROPIC_RESPONSE = {
    "id": "msg_01",
    "type": "message",
    "role": "assistant",
    "content": [
        {"type": "text", "text": "Looking that up."},
        {
            "type": "tool_use",
            "id": "toolu_xyz789",
            "name": "get_weather",
            "input": {"city": "Bengaluru", "units": "celsius"},
        },
    ],
    "stop_reason": "tool_use",
}

GEMINI_RESPONSE = {
    "candidates": [
        {
            "content": {
                "role": "model",
                "parts": [
                    {
                        "functionCall": {
                            "id": "fc-9a3d",
                            "name": "get_weather",
                            "args": {"city": "Bengaluru", "units": "celsius"},
                        }
                    }
                ],
            },
            "finishReason": "STOP",
        }
    ]
}

def parse_openai(resp: dict) -> List[Call]:
    msg = resp["choices"][0]["message"]
    calls = []
    for tc in msg.get("tool_calls", []):
        fn = tc["function"]
        calls.append(Call(id=tc["id"], name=fn["name"], args=json.loads(fn["arguments"])))
    return calls

def parse_anthropic(resp: dict) -> list[Call]:
    calls = []
    for block in resp.get("content", []):
        if block.get("type") == "tool_use":
            calls.append(Call(id=block["id"], name=block["name"], args=block["input"]))
    return calls

def parse_gemini(resp: dict) -> List[Call]:
    calls = []
    for part in resp["candidates"][0]["content"].get("parts", []):
        if "functionCall" in part:
            fc = part["functionCall"]
            calls.append(Call(id=fc.get("id", ""), name=fc["name"], args=fc["args"]))
    return calls


