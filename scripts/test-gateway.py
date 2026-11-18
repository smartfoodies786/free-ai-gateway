#!/usr/bin/env python3
"""Test a running FreeLLMAPI or OmniRoute gateway.

Lists /v1/models, then sends one tiny chat completion. Stdlib only.

  python3 scripts/test-gateway.py --gateway omniroute --api-key <unified-key>
  python3 scripts/test-gateway.py --gateway freellmapi --api-key <unified-key>
  python3 scripts/test-gateway.py --gateway omniroute --api-key <key> --models-only
  python3 scripts/test-gateway.py --base-url http://localhost:20128/v1 --api-key <key> --model auto

--gateway picks the known defaults:
  omniroute  -> http://localhost:20128/v1 , model "auto"
  freellmapi -> http://localhost:3001/v1  , model "auto"
Pass --base-url / --model to override. The key is the UNIFIED key from the
gateway dashboard (FreeLLMAPI: Keys page header; OmniRoute: Endpoints),
not a provider key.
"""
import argparse
import json
import sys
import urllib.error
import urllib.request

DEFAULTS = {
    "omniroute": ("http://localhost:20128/v1", "auto"),
    "freellmapi": ("http://localhost:3001/v1", "auto"),
}


def call(base_url, api_key, path, payload=None):
    url = base_url.rstrip("/") + path
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST" if payload is not None else "GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")[:500]
        return e.code, {"error": body}
    except Exception as e:  # gateway not running, connection refused, etc.
        return None, {"error": str(e)}


def main():
    p = argparse.ArgumentParser(description="Test a FreeLLMAPI / OmniRoute gateway")
    p.add_argument("--gateway", choices=list(DEFAULTS), default="omniroute")
    p.add_argument("--base-url", default=None)
    p.add_argument("--api-key", required=True, help="unified key from the dashboard")
    p.add_argument("--model", default=None)
    p.add_argument("--prompt", default="Say 'gateway OK' and nothing else.")
    p.add_argument("--models-only", action="store_true")
    args = p.parse_args()

    base_url, model = DEFAULTS[args.gateway]
    base_url = args.base_url or base_url
    model = args.model or model

    status, models = call(base_url, args.api_key, "/models")
    if status != 200:
        print(f"FAIL /v1/models -> {status}: {models}")
        return 1
    items = models.get("data", [])
    print(f"OK /v1/models -> {status}: {len(items)} models")
    for m in items[:10]:
        print("  -", m.get("id"))
    if args.models_only:
        return 0

    status, chat = call(
        base_url,
        args.api_key,
        "/chat/completions",
        {"model": model, "messages": [{"role": "user", "content": args.prompt}]},
    )
    if status != 200:
        print(f"FAIL /v1/chat/completions (model={model}) -> {status}: {chat}")
        return 1
    try:
        reply = chat["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        print(f"FAIL unexpected chat reply: {str(chat)[:500]}")
        return 1
    print(f"OK /v1/chat/completions (model={model}) -> {status}")
    print("Reply:", reply)
    usage = chat.get("usage")
    if usage:
        print("Usage:", usage)
    return 0


if __name__ == "__main__":
    sys.exit(main())
