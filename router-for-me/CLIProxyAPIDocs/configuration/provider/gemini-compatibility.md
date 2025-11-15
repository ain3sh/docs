# Gemini Compatibility Providers

Configure upstream Gemini compatible providers via `gemini-api-key`.

- api-key: API key for the provider
- base-url: provider base URL
- proxy-url: optional proxy URL for the provider
- headers: optional extra HTTP headers sent to the overridden Gemini endpoint only

Example:
```yaml
gemini-api-key:
  - api-key: "AIzaSy...01"
    base-url: "https://generativelanguage.googleapis.com"
    headers:
      X-Custom-Header: "custom-value"
    proxy-url: "socks5://proxy.example.com:1080"
  - api-key: "AIzaSy...02" # use the official Gemini API key, no need to set the base url
```

> [!NOTE]  
> If you set the `api-key` only, the `base-url` will be set to `https://generativelanguage.googleapis.com` automatically.   
> The `base-url` is only needed if you are using a third-party Gemini-compatible provider.
