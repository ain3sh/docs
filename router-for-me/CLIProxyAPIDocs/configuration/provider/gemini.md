# Gemini API Configuration

Use the `gemini-api-key` parameter to configure Gemini API keys. Each entry accepts optional `base-url`, `headers`, and `proxy-url` values; headers are only attached to requests sent to the overridden Gemini endpoint and are never forwarded to proxy servers. The legacy `generative-language-api-key` endpoint exposes a mirrored, key-only view for backwards compatibility—writes through that endpoint update the Gemini list but drop any per-key overrides, and the legacy field is no longer persisted in `config.yaml`.
