import os
import json
import urllib.request
from dotenv import load_dotenv

load_dotenv()
BASE_URL = 'https://openrouter.ai/api/v1'

def api_call_raw():
    api_key = os.environ.get('OPENROUTER_API_KEY')
    if not api_key:
        print('First set OPENROUTER_API_KEY variable')
        return

    model = os.environ.get("LLM_MODEL")
    if not model:
        print('First set LLM_MODEL variable')
        return

    url = f"{BASE_URL}/chat/completions"
    headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "User-Agent": 'agentic-ai-course/1.0'
            }
    body = json.dumps({
            "model": os.environ.get('LLM_MODEL'),
            "messages": [{
                "role": "user",
                "content": "how many r is in word 'strawberry'?"
                }],
            "reasoning": {"enabled": True}
        }).encode()

    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
            print(f"Raw HTTP response: {result['choices'][0]['message']['content']}")
            print(f"Tokens used: {result['usage']['prompt_tokens']} in {result['usage']['completion_tokens']} out")
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.code().decode()}")


if __name__ == "__main__":
    print("++ openrouter_api_call ++")
    api_call_raw()
