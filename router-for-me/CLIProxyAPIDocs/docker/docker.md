# Run with Docker

Run the following command to login (Gemini OAuth on port 8085):

```bash
docker run --rm -p 8085:8085 -v /path/to/your/config.yaml:/CLIProxyAPI/config.yaml -v /path/to/your/auth-dir:/root/.cli-proxy-api eceasy/cli-proxy-api:latest /CLIProxyAPI/CLIProxyAPI --login
```

Run the following command to login (OpenAI OAuth on port 1455):

```bash
docker run --rm -p 1455:1455 -v /path/to/your/config.yaml:/CLIProxyAPI/config.yaml -v /path/to/your/auth-dir:/root/.cli-proxy-api eceasy/cli-proxy-api:latest /CLIProxyAPI/CLIProxyAPI --codex-login
```

Run the following command to logi (Claude OAuth on port 54545):

```bash
docker run -rm -p 54545:54545 -v /path/to/your/config.yaml:/CLIProxyAPI/config.yaml -v /path/to/your/auth-dir:/root/.cli-proxy-api eceasy/cli-proxy-api:latest /CLIProxyAPI/CLIProxyAPI --claude-login
```

Run the following command to login (Qwen OAuth):

```bash
docker run -it -rm -v /path/to/your/config.yaml:/CLIProxyAPI/config.yaml -v /path/to/your/auth-dir:/root/.cli-proxy-api eceasy/cli-proxy-api:latest /CLIProxyAPI/CLIProxyAPI --qwen-login
```

Run the following command to login (iFlow OAuth on port 11451):

```bash
docker run --rm -p 11451:11451 -v /path/to/your/config.yaml:/CLIProxyAPI/config.yaml -v /path/to/your/auth-dir:/root/.cli-proxy-api eceasy/cli-proxy-api:latest /CLIProxyAPI/CLIProxyAPI --iflow-login
```

Run the following command to start the server:

```bash
docker run --rm -p 8317:8317 -v /path/to/your/config.yaml:/CLIProxyAPI/config.yaml -v /path/to/your/auth-dir:/root/.cli-proxy-api eceasy/cli-proxy-api:latest
```

> [!NOTE]
> To use the Git-backed configuration store with Docker, you can pass the `GITSTORE_*` environment variables using the `-e` flag. For example:
>
> ```bash
> docker run --rm -p 8317:8317 \
>   -e GITSTORE_GIT_URL="https://github.com/your/config-repo.git" \
>   -e GITSTORE_GIT_TOKEN="your_personal_access_token" \
>   -v /path/to/your/git-store:/CLIProxyAPI/remote \
>   eceasy/cli-proxy-api:latest
> ```
> In this case, you may not need to mount `config.yaml` or `auth-dir` directly, as they will be managed by the Git store inside the container at the `GITSTORE_LOCAL_PATH` (which defaults to `/CLIProxyAPI` and we are setting it to `/CLIProxyAPI/remote` in this example).
