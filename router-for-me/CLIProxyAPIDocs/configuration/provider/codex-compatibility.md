# Codex Compatibility Providers

Configure upstream Codex compatible providers via `codex-api-key`.

- api-key: API key for the provider
- base-url: provider base URL
- proxy-url: optional proxy URL for the provider

Example:
```yaml
codex-api-key:
  - api-key: "sk-atSM..."
    base-url: "https://www.example.com" # use the custom codex API endpoint
    proxy-url: "socks5://proxy.example.com:1080" # optional: per-key proxy override
```
