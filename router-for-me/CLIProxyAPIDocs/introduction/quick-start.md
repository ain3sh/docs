# Quick Start

## macOS

```bash
brew install cliproxyapi
brew services start cliproxyapi
```

## Linux

```bash
curl -fsSL https://raw.githubusercontent.com/brokechubb/cliproxyapi-installer/refs/heads/master/cliproxyapi-installer | bash
```

Thanks to [brokechubb](https://github.com/brokechubb) for building the Linux installer!

## Windows

You can download the latest release from [here](https://github.com/router-for-me/CLIProxyAPI/releases) and run it directly.

Or

You can download our desktop GUI app from [here](https://github.com/router-for-me/EasyCLI/releases) and run it directly.

## Docker

```bash
docker run --rm -p 8317:8317 -v /path/to/your/config.yaml:/CLIProxyAPI/config.yaml -v /path/to/your/auth-dir:/root/.cli-proxy-api eceasy/cli-proxy-api:latest
```

## Building from Source

1. Clone the repository:
   ```bash
   git clone https://github.com/router-for-me/CLIProxyAPI.git
   cd CLIProxyAPI
   ```

2. Build the application:

   Linux, macOS:
   ```bash
   go build -o cli-proxy-api ./cmd/server
   ```
   Windows:
   ```bash
   go build -o cli-proxy-api.exe ./cmd/server
   ```
