# Documentation References

A curated collection of documentation mirrors with automated semantic search indexing.

<!-- AUTO:MIRROR_STATUS -->
## Mirror Status

| Mirror | Upstream | Branch | Docs Path | Last Commit | Synced At |
| --- | --- | --- | --- | --- | --- |
| Factory-AI/factory | [https://github.com/Factory-AI/factory](https://github.com/Factory-AI/factory) | main | docs | 57c2897 | 2025-11-17T19:28:24+00:00Z |
| openai/codex | [https://github.com/openai/codex](https://github.com/openai/codex) | main | docs | 03a6e85 | 2025-11-17T20:03:33+00:00Z |
| stanfordnlp/dspy | [https://github.com/stanfordnlp/dspy](https://github.com/stanfordnlp/dspy) | main | docs | a5671ef | 2025-11-17T19:28:22+00:00Z |
| lastmile-ai/mcp-agent | [https://github.com/lastmile-ai/mcp-agent](https://github.com/lastmile-ai/mcp-agent) | main | docs | ccaab49 | 2025-11-17T19:28:21+00:00Z |
| MoonshotAI/kosong | [https://github.com/MoonshotAI/kosong](https://github.com/MoonshotAI/kosong) | main | src/kosong | 4c25822 | 2025-11-17T19:28:21+00:00Z |
| modelcontextprotocol/modelcontextprotocol | [https://github.com/modelcontextprotocol/modelcontextprotocol](https://github.com/modelcontextprotocol/modelcontextprotocol) | main | docs/docs | 0678e68 | 2025-11-17T19:28:21+00:00Z |
| ericbuess/claude-code-docs | [https://github.com/ericbuess/claude-code-docs](https://github.com/ericbuess/claude-code-docs) | main | docs | 104457c | 2025-11-17T19:28:21+00:00Z |
| anthropics/claude-agent-sdk-python | [https://github.com/anthropics/claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python) | main | examples | ff425b2 | 2025-11-17T19:28:21+00:00Z |
| browserbase/sdk-python | [https://github.com/browserbase/sdk-python](https://github.com/browserbase/sdk-python) | main | examples | f6e0241 | 2025-11-17T19:28:22+00:00Z |
| browser-use/browser-use | [https://github.com/browser-use/browser-use](https://github.com/browser-use/browser-use) | main | docs | de06544 | 2025-11-17T19:28:22+00:00Z |
| browser-use/workflow-use | [https://github.com/browser-use/workflow-use](https://github.com/browser-use/workflow-use) | main | workflows | 680f5d3 | 2025-11-17T19:28:22+00:00Z |
| python-trio/trio | [https://github.com/python-trio/trio](https://github.com/python-trio/trio) | main | docs/source | 107048d | 2025-11-17T19:28:22+00:00Z |
| metatool-ai/metamcp | [https://github.com/metatool-ai/metamcp](https://github.com/metatool-ai/metamcp) | main | docs/en | 8dc10e9 | 2025-11-17T19:28:22+00:00Z |
| router-for-me/CLIProxyAPIDocs | [https://github.com/router-for-me/CLIProxyAPIDocs](https://github.com/router-for-me/CLIProxyAPIDocs) | main | docs/en | 5c0889d | 2025-11-17T19:28:23+00:00Z |
<!-- /AUTO:MIRROR_STATUS -->

<!-- AUTO:SEMANTIC_SEARCH -->
## Semantic Search

This repository includes automated indexing for Gemini File Search API.

- **Stores updated**: 1
- **Files indexed**: 20
- **Total cost**: $0.0045
- **Last sync**: 2025-11-17T20:05:21+00:00Z

Use the [search-context MCP server](https://github.com/ain3sh/search-context) to query these docs semantically.
<!-- /AUTO:SEMANTIC_SEARCH -->

<!-- AUTO:REPOSITORY_TREE -->
## Repository Tree

```text
.
├── anthropics
│   └── claude-agent-sdk-python
├── browser-use
│   ├── browser-use
│   └── workflow-use
├── browserbase
│   └── sdk-python
├── ericbuess
│   └── claude-code-docs
├── Factory-AI
│   └── factory
├── lastmile-ai
│   └── mcp-agent
├── metatool-ai
│   └── metamcp
├── modelcontextprotocol
│   └── modelcontextprotocol
├── MoonshotAI
│   └── kosong
├── openai
│   └── codex
├── python-trio
│   └── trio
├── router-for-me
│   └── CLIProxyAPIDocs
├── stanfordnlp
│   └── dspy
├── unstructured
├── .gitignore
├── .reference-sync
├── LICENSE
├── mirrors.json
└── README.md
````

<!-- /AUTO:REPOSITORY_TREE -->

## Configuration

### Adding Mirrors

Edit `mirrors.json` (validated against [`.github/mirrors.schema.json`](./.github/mirrors.schema.json)):

```json
{
  "mirrors": [
    {
      "owner": "github-user",
      "repo": "repository-name",
      "branch": "main",
      "docsPath": "docs"
    }
  ]
}
```

### Excluding from Search Index

Add directories to `geminiExclusions` to prevent indexing:

```json
{
  "geminiExclusions": [
    "archived",
    "temp/*",
    "private-notes"
  ]
}
```

Pattern types:

* **Exact**: `"unstructured"` → excludes `unstructured/`
* **Prefix**: `"temp/*"` → excludes anything starting with `temp/`

### Workflow

* **Automatic sync**: Daily at 3 AM UTC
* **Manual trigger**: GitHub Actions → “Sync Documentation References” → “Run workflow”
* **On config change**: Automatically runs when `mirrors.json` is updated

### Forking

To use this setup for your own documentation:

1. Fork this repository.
2. Clear `mirrors.json` and add your own mirrors.
3. Set GitHub Actions secrets:

   * `GEMINI_API_KEY` (required) – get from Google AI Studio.
   * `MIRROR_GIT_TOKEN` (optional) – only needed for private repos or rate-limit issues.
4. Let the workflows run automatically.

The `ask-docs-agent` MCP tool will automatically discover and index your mirrors.
