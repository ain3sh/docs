# Claude Code Compatibility Providers

Configure upstream Claude Code compatible providers via `claude-api-key`.

- api-key: API key for the provider
- base-url: provider base URL
- proxy-url: optional proxy URL for the provider
- models: list of mappings from upstream model `name` to local `alias`

Example:
```yaml
claude-api-key:
  - api-key: "sk-atSM..." # use the official claude API key, no need to set the base url
  - api-key: "sk-atSM..."
    base-url: "https://www.example.com" # use the custom claude API endpoint
    proxy-url: "socks5://proxy.example.com:1080" # optional: per-key proxy override
    models:
      - name: "claude-3-5-sonnet-20241022" # upstream model name
        alias: "claude-sonnet-latest" # client alias mapped to the upstream model
```

> [!NOTE]  
> If you set the `api-key` only, the `base-url` will be set to `https://api.anthropic.com` automatically.   
> The `base-url` is only needed if you are using a third-party Claude Code compatible provider.
