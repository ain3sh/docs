# Documentation References

A curated collection of documentation mirrors with automated semantic search indexing.

<!-- AUTO:MIRROR_STATUS -->
## Mirror Status

| Mirror | Upstream | Branch | Docs Path | Last Commit | Synced At |
| --- | --- | --- | --- | --- | --- |
| Factory-AI/factory | [https://github.com/Factory-AI/factory](https://github.com/Factory-AI/factory) | main | docs | eab7e4b | 2025-12-07T03:58:23+00:00Z |
| openai/codex | [https://github.com/openai/codex](https://github.com/openai/codex) | main | docs | b2cb05d | 2025-12-07T03:58:20+00:00Z |
| stanfordnlp/dspy | [https://github.com/stanfordnlp/dspy](https://github.com/stanfordnlp/dspy) | main | docs | b6115d4 | 2025-12-06T03:43:57+00:00Z |
| lastmile-ai/mcp-agent | [https://github.com/lastmile-ai/mcp-agent](https://github.com/lastmile-ai/mcp-agent) | main | docs | 2c377ac | 2025-12-06T03:43:55+00:00Z |
| MoonshotAI/kosong | [https://github.com/MoonshotAI/kosong](https://github.com/MoonshotAI/kosong) | main | src/kosong | 88828bd | 2025-12-07T03:58:20+00:00Z |
| modelcontextprotocol/modelcontextprotocol | [https://github.com/modelcontextprotocol/modelcontextprotocol](https://github.com/modelcontextprotocol/modelcontextprotocol) | main | docs/docs | 33576f5 | 2025-12-07T03:58:20+00:00Z |
| ericbuess/claude-code-docs | [https://github.com/ericbuess/claude-code-docs](https://github.com/ericbuess/claude-code-docs) | main | docs | 15e3ade | 2025-12-07T03:58:20+00:00Z |
| anthropics/claude-agent-sdk-python | [https://github.com/anthropics/claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python) | main | examples | 5625286 | 2025-12-07T03:58:21+00:00Z |
| browserbase/sdk-python | [https://github.com/browserbase/sdk-python](https://github.com/browserbase/sdk-python) | main | examples | f6e0241 | 2025-11-17T21:32:12+00:00Z |
| browser-use/browser-use | [https://github.com/browser-use/browser-use](https://github.com/browser-use/browser-use) | main | docs | b02ff05 | 2025-12-05T03:53:13+00:00Z |
| browser-use/workflow-use | [https://github.com/browser-use/workflow-use](https://github.com/browser-use/workflow-use) | main | workflows | cb8fea7 | 2025-11-20T03:45:08+00:00Z |
| python-trio/trio | [https://github.com/python-trio/trio](https://github.com/python-trio/trio) | main | docs/source | 5cefcd3 | 2025-12-06T03:43:56+00:00Z |
| metatool-ai/metamcp | [https://github.com/metatool-ai/metamcp](https://github.com/metatool-ai/metamcp) | main | docs/en | c0ff012 | 2025-12-07T03:58:21+00:00Z |
| router-for-me/CLIProxyAPIDocs | [https://github.com/router-for-me/CLIProxyAPIDocs](https://github.com/router-for-me/CLIProxyAPIDocs) | main | docs/en | c80c37c | 2025-12-07T03:58:21+00:00Z |
| raycast/extensions | [https://github.com/raycast/extensions](https://github.com/raycast/extensions) | main | docs | e0d4df7 | 2025-12-06T03:43:58+00:00Z |
<!-- /AUTO:MIRROR_STATUS -->

<!-- AUTO:SEMANTIC_SEARCH -->
## Semantic Search

This repository includes automated indexing for Gemini File Search API.

- **Stores updated**: 7
- **Files indexed**: 384
- **Total cost**: $0.1023
- **Last sync**: 2025-12-07T03:59:07+00:00Z

Use the [search-context MCP server](https://github.com/ain3sh/search-context) to query these docs semantically.
<!-- /AUTO:SEMANTIC_SEARCH -->

<!-- AUTO:REPOSITORY_TREE -->
## Repository Tree

```
.
├── anthropics
│   └── claude-agent-sdk-python
│       ├── plugins
│       ├── agents.py
│       ├── hooks.py
│       ├── include_partial_messages.py
│       ├── max_budget_usd.py
│       ├── mcp_calculator.py
│       ├── plugin_example.py
│       ├── quick_start.py
│       ├── setting_sources.py
│       ├── stderr_callback_example.py
│       ├── streaming_mode.py
│       ├── streaming_mode_ipython.py
│       ├── streaming_mode_trio.py
│       ├── system_prompt.py
│       ├── tool_permission_callback.py
│       └── tools_option.py
├── browser-use
│   ├── browser-use
│   │   ├── customize
│   │   ├── development
│   │   ├── examples
│   │   ├── images
│   │   ├── logo
│   │   ├── development.mdx
│   │   ├── docs.json
│   │   ├── favicon.ico
│   │   ├── favicon.svg
│   │   ├── introduction.mdx
│   │   ├── production.mdx
│   │   ├── quickstart.mdx
│   │   ├── quickstart_llm.mdx
│   │   ├── README.md
│   │   └── supported-models.mdx
│   └── workflow-use
│       ├── backend
│       ├── docs
│       ├── examples
│       ├── storage
│       ├── tests
│       ├── workflow_use
│       ├── .env.example
│       ├── .gitignore
│       ├── .python-version
│       ├── cli.py
│       ├── migrate_json_to_yaml.py
│       ├── pyproject.toml
│       ├── README.md
│       ├── test_max_alternatives_bug_fix.py
│       └── uv.lock
├── browserbase
│   └── sdk-python
│       ├── e2e
│       ├── packages
│       ├── .keep
│       ├── __init__.py
│       ├── playwright_basic.py
│       ├── playwright_captcha.py
│       ├── playwright_contexts.py
│       ├── playwright_downloads.py
│       ├── playwright_extensions.py
│       ├── playwright_proxy.py
│       ├── playwright_upload.py
│       └── selenium_basic.py
├── ericbuess
│   └── claude-code-docs
│       ├── amazon-bedrock.md
│       ├── analytics.md
│       ├── changelog.md
│       ├── checkpointing.md
│       ├── claude-code-on-the-web.md
│       ├── cli-reference.md
│       ├── common-workflows.md
│       ├── costs.md
│       ├── data-usage.md
│       ├── desktop.md
│       ├── devcontainer.md
│       ├── docs_manifest.json
│       ├── github-actions.md
│       ├── gitlab-ci-cd.md
│       ├── google-vertex-ai.md
│       ├── headless.md
│       ├── hooks-guide.md
│       ├── hooks.md
│       ├── iam.md
│       ├── interactive-mode.md
│       ├── jetbrains.md
│       ├── legal-and-compliance.md
│       ├── llm-gateway.md
│       ├── mcp.md
│       ├── memory.md
│       ├── microsoft-foundry.md
│       ├── model-config.md
│       ├── monitoring-usage.md
│       ├── network-config.md
│       ├── output-styles.md
│       ├── overview.md
│       ├── plugin-marketplaces.md
│       ├── plugins-reference.md
│       ├── plugins.md
│       ├── quickstart.md
│       ├── sandboxing.md
│       ├── sdk__migration-guide.md
│       ├── security.md
│       ├── settings.md
│       ├── setup.md
│       ├── skills.md
│       ├── slash-commands.md
│       ├── statusline.md
│       ├── sub-agents.md
│       ├── terminal-config.md
│       ├── third-party-integrations.md
│       ├── troubleshooting.md
│       └── vs-code.md
├── Factory-AI
│   └── factory
│       ├── changelog
│       ├── cli
│       ├── enterprise
│       ├── guides
│       ├── images
│       ├── logo
│       ├── onboarding
│       ├── reference
│       ├── web
│       ├── welcome
│       ├── convert_md_to_mdx.sh
│       ├── docs.json
│       ├── factory-docs-map.mdx
│       ├── factoryhomepage.png
│       ├── favicon.svg
│       ├── pricing.mdx
│       ├── README.md
│       └── style.css
├── lastmile-ai
│   └── mcp-agent
│       ├── advanced
│       ├── cloud
│       ├── concepts
│       ├── css
│       ├── get-started
│       ├── images
│       ├── logo
│       ├── mcp
│       ├── mcp-agent-sdk
│       ├── openai
│       ├── reference
│       ├── snippets
│       ├── test-evaluate
│       ├── workflows
│       ├── configuration.mdx
│       ├── docs.json
│       ├── favicon.png
│       ├── oauth_support_design.md
│       ├── README.md
│       └── roadmap.mdx
├── metatool-ai
│   └── metamcp
│       ├── concepts
│       ├── deployment
│       ├── development
│       ├── integrations
│       ├── troubleshooting
│       ├── index.mdx
│       └── quickstart.mdx
├── modelcontextprotocol
│   └── modelcontextprotocol
│       ├── develop
│       ├── getting-started
│       ├── learn
│       ├── tools
│       ├── tutorials
│       └── sdk.mdx
├── MoonshotAI
│   └── kosong
│       ├── chat_provider
│       ├── contrib
│       ├── tooling
│       ├── utils
│       ├── __init__.py
│       ├── __main__.py
│       ├── _generate.py
│       ├── message.py
│       └── py.typed
├── openai
│   └── codex
│       ├── advanced.md
│       ├── agents_md.md
│       ├── authentication.md
│       ├── CLA.md
│       ├── config.md
│       ├── contributing.md
│       ├── example-config.md
│       ├── exec.md
│       ├── execpolicy.md
│       ├── experimental.md
│       ├── faq.md
│       ├── getting-started.md
│       ├── install.md
│       ├── license.md
│       ├── open-source-fund.md
│       ├── platform-sandboxing.md
│       ├── prompts.md
│       ├── release_management.md
│       ├── sandbox.md
│       ├── skills.md
│       ├── slash_commands.md
│       ├── windows_sandbox_security.md
│       └── zdr.md
├── python-trio
│   └── trio
│       ├── _static
│       ├── _templates
│       ├── reference-core
│       ├── reference-testing
│       ├── tutorial
│       ├── awesome-trio-libraries.rst
│       ├── code-of-conduct.rst
│       ├── conf.py
│       ├── contributing.rst
│       ├── design.rst
│       ├── glossary.rst
│       ├── history.rst
│       ├── index.rst
│       ├── local_customization.py
│       ├── reference-core.rst
│       ├── reference-io.rst
│       ├── reference-lowlevel.rst
│       ├── reference-testing.rst
│       ├── releasing.rst
│       ├── tutorial.rst
│       └── typevars.py
├── raycast
│   └── extensions
│       ├── .gitbook
│       ├── ai
│       ├── api-reference
│       ├── basics
│       ├── examples
│       ├── information
│       ├── migration
│       ├── teams
│       ├── utils-reference
│       ├── .config.json
│       ├── .gitbook.yaml
│       ├── .prettierrc
│       ├── changelog.md
│       ├── faq.md
│       ├── README.md
│       └── SUMMARY.md
├── router-for-me
│   └── CLIProxyAPIDocs
│       ├── agent-client
│       ├── configuration
│       ├── docker
│       ├── hands-on
│       ├── introduction
│       ├── management
│       └── index.md
├── stanfordnlp
│   └── dspy
│       ├── docs
│       ├── overrides
│       ├── scripts
│       ├── .gitignore
│       ├── mkdocs.yml
│       ├── Pipfile
│       ├── Pipfile.lock
│       ├── README.md
│       ├── requirements.txt
│       └── vercel.json
├── unstructured
│   ├── ai.google.dev_gemini-api_docs_file-search.2025-11-09T18_08_25.315Z.md
│   ├── blog.google_technology_developers_file-search-gemini-api_.2025-11-09T18_07_43.675Z.md
│   ├── CONTEXT_SEARCH_MCP_SPEC.md
│   └── nodejs.org_api_single-executable-applications.html.2025-11-09T19_17_34.546Z.md
├── .gitignore
├── .reference-sync
├── LICENSE
├── mirrors.json
└── README.md
```
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
