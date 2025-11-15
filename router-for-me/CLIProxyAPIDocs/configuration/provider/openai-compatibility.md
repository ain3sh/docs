# OpenAI Compatibility Providers

Configure upstream OpenAI-compatible providers (e.g., OpenRouter) via `openai-compatibility`.

- name: provider identifier used internally
- base-url: provider base URL
- api-key-entries: list of API key entries with optional per-key proxy configuration (recommended)
- api-keys: (deprecated) simple list of API keys without proxy support
- models: list of mappings from upstream model `name` to local `alias`

Example with per-key proxy support:

```yaml
openai-compatibility:
  - name: "openrouter"
    base-url: "https://openrouter.ai/api/v1"
    api-key-entries:
      - api-key: "sk-or-v1-...b780"
        proxy-url: "socks5://proxy.example.com:1080"
      - api-key: "sk-or-v1-...b781"
    models:
      - name: "moonshotai/kimi-k2:free"
        alias: "kimi-k2"
```

Usage:

Call OpenAI's endpoint `/v1/chat/completions` with `model` set to the alias (e.g., `kimi-k2`). The proxy routes to the configured provider/model automatically.
