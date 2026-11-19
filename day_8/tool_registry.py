from dataclasses import dataclass
from typing import Any, Callable
import datetime as dt

MAX_TURNS = 5

@dataclass
class Tool:
    name: str
    description: str
    input_schema: dict
    executor: Callable[[dict], Any]
    consequential: bool = False

def tool_add(args: dict) -> dict:
    return {"sum": args["a"] + args["b"]}

def tool_get_time(args: dict) -> dict:
    tz = args.get("timezone", "UTC")
    now = dt.datetime.now(dt.timezone.utc).isoformat(timespace="seconds")
    return {"now": now, "timezone": tz}

def tool_get_weather(args: dict) -> dict:
    fake = {"Bengaluru": 28, "Tokyo": 12, "Delhi": 18}
    city = args["city"]
    units = args.get("units", "celsius")
    temp = fake.get(city, 20)
    return {"city": city, "temp": temp, "units": units}

REGISTRY: list[Tool] = [
    Tool(
        name="add",
        description=(
            "Use when the user asks for the sum of two numbers. \n"
            "Do not use for subtraction, product, or symbolic algebra."
        ),
        input_schema={
            "type": "object",
            "properties": {
                "a": {"type": "number"},
                "b": {"type": "number"},
            },
            "required": ["a", "b"]
        },
        executor=tool_add
    ),
    Tool(
        name="get_weather",
        description=(
            "Use when the user asks about current conditions in a named city. \n"
            "Do not use for forecasts or historical weather data."
        ),
        input_schema={
            "type": "object",
            "properties": {
                "city": {"type": "string"},
                "units": {"type": "string", "enum": ["celsius", "fahrenheit"]},
            },
            "required": ["city"]
        },
        executor=tool_get_weather,
    ),
    Tool(
        name="get_time",
        description=(
            "Use when the user asks what time it is. \n"
            "Do not use for historical dates or future scheduling."
        ),
        input_schema={
            "type": "object",
            "properties": {
                "timezone": {"type": "string"}            
            },
            "required": ["city"]
        },
        executor=tool_get_time,
    ),
]
