import json
import time
import hashlib
import requests
from dotenv import load_dotenv
import os

api_key = os.environ.get("OPENROUTER_API_KEY")

MODEL_CONFIGS = {
    "google/gemma-4-31b-it:free": {
        "provider": "openrouter",
        "model": "google/gemma-4-31b-it:free",
        "max_tokens": 32768,
        "context_window": 262144,
    },
    "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free": {
        "provider": "openrouter",
        "model": "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
        "max_tokens": 65536,
        "context_window": 256000,
    },
    "nvidia/nemotron-3.5-super-vl:free": {
        "provider": "openrouter",
        "model": "nvidia/nemotron-3.5-super-vl:free",
        "max_tokens": 131072,
        "context_window": 1000000,
    },
}

def format_openrouter_request(prompt, model):
    return {
        "model": MODEL_CONFIGS[model]["model"],
        "messages": [
            { "role": "system", "content": prompt["system"] },
            { "role": "user", "content": prompt["user"] },
        ],
        "temperature": prompt["temperature"],
        "max_tokens": MODEL_CONFIGS[model]["max_tokens"]
    }

def llm_call(message):
    response = requests.post(
        url = "https://openrouter.ai/api/v1/chat/completions",
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=message,
        timeout=120
    )

    response.raise_for_status()
    result = response.json()
    assistant_response = result["choices"][0]["content"]

    usage = result.get("usage", {})
    latency_ms = round((time.time() - start_time) * 1000, 2)

    return {
        "response": assistant_response,
        "tokens_used": {
            "prompt": usage.get("prompt_tokens", 0),
            "completion": usage.get("completions_tokens", 0),
            "total": usage.get("total_tokens", 0),
        },
        "latency_ms": latency_ms,
        "finish_reason": result["choices"][0].get("finish_reason"),
        "model": result.get("model")
    }

def run_prompt_test(prompt, models=None):
    if models is None:
        models = list(MODEL_CONFIGS.keys())

    results = {}
    for model_name in models:
        message = format_openrouter_request(prompt, model_name)
        response = llm_call(message)
        results[model_name] = response

    return results
