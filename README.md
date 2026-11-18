# Free AI Gateway — FreeLLMAPI + OmniRoute in one repo

One Docker Compose stack that gives you **one API endpoint** for all your
free AI keys, with automatic failover when one provider hits its limit.

Source video: [AI With Ankit — "AI ki limit khatam? Har mahine ~11 billion AI tokens free"](https://www.facebook.com/reel/1889309552519348/)
— two free tools: **FreeLLMAPI** + **OmniRoute**. This repo is that system,
built so you can actually run it.

## The honest maths first

| | FreeLLMAPI | OmniRoute |
|---|---|---|
| Listed free capacity | ~10.1B tokens/mo | ~1.62B tokens/mo |
| Providers | 87 | 375 (150+ free) |
| Models / endpoints | 1,313 endpoints | 1,400+ models |
| GitHub stars (18 Nov 2026) | 54,266 — `tashfeenahmed/freellmapi` | 88,517 — `cheaper-inference/OmniRoute` |
| Extra trick | Smart routing + failover, `/v1/messages` for Claude Code | Token compression 15–95% (RTK → Caveman, ~89% avg on tool-heavy coding) |

**11 billion is a sum, not a grant.** Nobody gives you 11B tokens. Each
provider gives its own small free tier; the gateways stack them behind one
endpoint. You still need your own free key per provider (see
`keys-checklist.md` — start with the 5 there).

Also honest: the free models are Gemini, Mistral, GLM, Qwen, DeepSeek and
similar — **not real Claude or GPT**. They do everyday chat, coding help
and agent work well, but they are not Claude. And both upstreams say it
plainly: **personal experimentation and learning, not production**. Late in
the day the best free models hit their daily caps and quality dips until
the UTC-midnight reset — that is normal, the failover just moves you to
the next provider.

## Quick start (PC / laptop, Docker)

```bash
git clone https://github.com/smartfoodies786/free-ai-gateway.git
cd free-ai-gateway
cp .env.example .env
docker compose up -d
```

Then open the dashboards and add your keys:

| Gateway | Dashboard | API endpoint | Unified key |
|---|---|---|---|
| FreeLLMAPI | http://localhost:3001 | http://localhost:3001/v1 | Keys page header (`freellmapi-...`) |
| OmniRoute | http://localhost:20128 | http://localhost:20128/v1 | Dashboard → Endpoints |

Low-RAM PC? Start only one gateway: `docker compose up -d omniroute`
or `docker compose up -d freellmapi`. Coding agents on OmniRoute need
`OMNIROUTE_MEMORY_MB=8192` and ~10 GB RAM (upstream guide); light chat
works with 1024.

No Docker? OmniRoute alone: `npm install -g omniroute && omniroute`.
FreeLLMAPI alone: `curl -fsSL https://freellmapi.co/install.sh | bash`
then open http://localhost:3001. On Windows the easiest FreeLLMAPI path
is the desktop app from the Microsoft Store.

## Test it

```bash
python3 scripts/test-gateway.py --gateway omniroute --api-key <unified-key>
python3 scripts/test-gateway.py --gateway freellmapi --api-key <unified-key>
```

It lists `/v1/models`, then sends one tiny chat call and prints the reply.
If the gateway is not running you get `FAIL` with the connection error —
start the stack first, then re-run.

One chat call from your own code — see `examples/chat.py`:

```bash
export FREEGATEWAY_BASE_URL=http://localhost:20128/v1
export FREEGATEWAY_API_KEY=<unified-key-from-dashboard>
export FREEGATEWAY_MODEL=auto
python3 examples/chat.py "Explain Groq vs Gemini in 2 lines"
```

## Use it in Claude Code / Cursor

**Claude Code → FreeLLMAPI** (verified upstream command):

```bash
FREELLMAPI_API_KEY=<unified-key> bash scripts/setup-claude-code.sh
# same as: npx freellmapi setup-claude --url http://localhost:3001 --api-key <unified-key>
```

**Any OpenAI-compatible client → OmniRoute:**

```
Base URL: http://localhost:20128/v1
API Key:  copy from Dashboard → Endpoints
Model:    auto
```

Cursor, Codex CLI, Cline, Roo Code, Continue, Aider and OpenCode all take
the same Base URL + key + model. FreeLLMAPI also has setup generators for
them (`npx freellmapi setup-codex`, `setup-aider`, `setup-cursor`, …).

## Files

- `docker-compose.yml` — both gateways, localhost-only, healthchecks
- `scripts/test-gateway.py` — stdlib-only gateway test (models + 1 chat)
- `scripts/setup-claude-code.sh` — Claude Code → FreeLLMAPI wiring
- `examples/chat.py` — copy-paste template for your own apps
- `keys-checklist.md` — the 5 free keys to get first, and what to avoid

## Roman Urdu — 3 steps

1. **Repo clone karo, `docker compose up -d` chalao.**
2. **Dono dashboards kholo** (3001 aur 20128), apni 5 free keys add karo
   — Groq wali pehle se hai, dobara banane ki zaroorat nahi.
3. **`python3 scripts/test-gateway.py --gateway omniroute --api-key <key>`**
   — `OK` aaya to system live hai, phir Claude Code / Cursor mein
   upar wala Base URL laga do.

Keys kabhi chat mein ya repo mein mat likhna — sirf dashboard mein.
