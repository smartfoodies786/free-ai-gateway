# Keys checklist — get these 5 first

The gateways add NO free tokens by themselves. They stack the free tiers
you sign up for. Add each key in the dashboard (FreeLLMAPI: Keys page,
OmniRoute: Providers page). Never paste a key in chat or in this repo.

Tick them off in this order — fastest useful pool first:

- [ ] **1. Groq** — you already have a Groq key (EduPlay / Workar bots use
  it). Reuse it here; do NOT paste it anywhere to get it in. Fastest free
  models, per-model daily caps.
- [ ] **2. Google AI Studio (Gemini)** — free tier, big models, the
  workhorse for everyday chat + coding help.
- [ ] **3. Cerebras** — very fast free inference, good second fallback.
- [ ] **4. Mistral** — large free pool (OmniRoute counts ~1B tokens/mo
  from Mistral alone). Note: Mistral's free credit has changed before —
  check its current free tier on its own site when you sign up.
- [ ] **5. OpenRouter** — `:free` models only. No card for the free
  models; paid top-up is optional and NOT needed for this system.

Later, only if you need more: NVIDIA NIM, Z.ai (Zhipu), Cloudflare
Workers AI, HuggingFace. The full catalog lives at freellmapi.co/models
and in the OmniRoute dashboard under `/dashboard/free-tiers`.

## Do NOT use

- **Cohere** — FreeLLMAPI's own terms review rates it "avoid": its terms
  forbid personal / household use. Skip it.
- **Any key you did not create yourself**, or a "shared" key from a
  video / comment / Telegram group. Those get revoked and can get the
  account banned.
- **Production apps on this pool.** Both upstreams say the same thing:
  personal experimentation and learning, not production. If a bot or site
  starts earning, swap that one to a paid key before you ship it.
