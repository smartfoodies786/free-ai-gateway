#!/usr/bin/env python3
"""One chat call through either gateway. Stdlib only, no dependencies.

  export FREEGATEWAY_BASE_URL=http://localhost:20128/v1   # OmniRoute
  # or: export FREEGATEWAY_BASE_URL=http://localhost:3001/v1  # FreeLLMAPI
  export FREEGATEWAY_API_KEY=<unified-key-from-dashboard>
  export FREEGATEWAY_MODEL=auto
  python3 examples/chat.py "Explain Groq vs Gemini in 2 lines"

Use this as the template for your own apps (EduPlay, Workar bots, etc):
point the OpenAI-compatible client at FREEGATEWAY_BASE_URL with the
unified key, and the gateway routes + fails over across your free keys.
"""
import json
import os
import sys
import urllib.request

BASE_URL = os.environ.get("FREEGATEWAY_BASE_URL", "http://localhost:20128/v1")
API_KEY = os.environ.get("FREEGATEWAY_API_KEY", "")
MODEL = os.environ.get("FREEGATEWAY_MODEL", "auto")


def chat(prompt, model=MODEL):
    if not API_KEY:
        raise SystemExit("Set FREEGATEWAY_API_KEY to the unified key from the dashboard.")
    payload = json.dumps(
        {"model": model, "messages": [{"role": "user", "content": prompt}]}
    ).encode()
    req = urllib.request.Request(
        BASE_URL.rstrip("/") + "/chat/completions",
        data=payload,
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        body = json.loads(resp.read().decode())
    return body["choices"][0]["message"]["content"]


if __name__ == "__main__":
    prompt = " ".join(sys.argv[1:]) or "Say 'gateway OK' and nothing else."
    print(chat(prompt))
