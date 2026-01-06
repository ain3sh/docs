# Documentation References

A curated collection of documentation mirrors with automated semantic search indexing.

<!-- AUTO:MIRROR_STATUS -->
## Mirror Status

| Mirror | Upstream | Branch | Docs Path | Last Commit | Synced At |
| --- | --- | --- | --- | --- | --- |
| Factory-AI/factory | [https://github.com/Factory-AI/factory](https://github.com/Factory-AI/factory) | main | docs | e85e1c6 | 2026-01-05T21:10:01+00:00Z |
| stanfordnlp/dspy | [https://github.com/stanfordnlp/dspy](https://github.com/stanfordnlp/dspy) | main | docs | becb4c9 | 2026-01-05T21:09:59+00:00Z |
| lastmile-ai/mcp-agent | [https://github.com/lastmile-ai/mcp-agent](https://github.com/lastmile-ai/mcp-agent) | main | docs | 04cae7e | 2026-01-05T21:09:58+00:00Z |
| MoonshotAI/kimi-cli | [https://github.com/MoonshotAI/kimi-cli](https://github.com/MoonshotAI/kimi-cli) | main | packages/kosong/src/kosong | 8007d2f | 2026-01-05T21:09:58+00:00Z |
| modelcontextprotocol/modelcontextprotocol | [https://github.com/modelcontextprotocol/modelcontextprotocol](https://github.com/modelcontextprotocol/modelcontextprotocol) | main | docs/docs | e32d742 | 2026-01-06T04:03:17+00:00Z |
| modelcontextprotocol/python-sdk | [https://github.com/modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk) | main | docs | bb6cb02 | 2026-01-05T21:10:00+00:00Z |
| ericbuess/claude-code-docs | [https://github.com/ericbuess/claude-code-docs](https://github.com/ericbuess/claude-code-docs) | main | docs | cb41493 | 2026-01-06T04:03:17+00:00Z |
| anthropics/claude-agent-sdk-python | [https://github.com/anthropics/claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python) | main | examples | 23c9df3 | 2026-01-05T21:10:00+00:00Z |
| browser-use/browser-use | [https://github.com/browser-use/browser-use](https://github.com/browser-use/browser-use) | main | docs | c9b6fe7 | 2026-01-05T21:10:01+00:00Z |
| browser-use/workflow-use | [https://github.com/browser-use/workflow-use](https://github.com/browser-use/workflow-use) | main | workflows | cb8fea7 | 2026-01-05T21:10:01+00:00Z |
| python-trio/trio | [https://github.com/python-trio/trio](https://github.com/python-trio/trio) | main | docs/source | befe650 | 2026-01-06T04:03:17+00:00Z |
| raycast/extensions | [https://github.com/raycast/extensions](https://github.com/raycast/extensions) | main | docs | 8534452 | 2026-01-06T04:03:18+00:00Z |
<!-- /AUTO:MIRROR_STATUS -->

<!-- AUTO:SEMANTIC_SEARCH -->
## Semantic Search

This repository includes automated indexing for Gemini File Search API.

- **Stores**: 12
- **Files indexed**: 716
- **Total cost**: $0.2161
- **Last sync**: 2026-01-06T04:03:41+00:00Z

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
│       ├── filesystem_agents.py
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
│       │   ├── __init__.py
│       │   ├── README.md
│       │   ├── test_playwright.py
│       │   └── test_selenium.py
│       ├── packages
│       │   ├── extensions
│       │   │   ├── browserbase-test
│       │   │   │   ├── images
│       │   │   │   │   └── logo.png
│       │   │   │   ├── scripts
│       │   │   │   │   └── content.js
│       │   │   │   ├── hello.html
│       │   │   │   └── manifest.json
│       │   │   └── .gitignore
│       │   └── logo.png
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
│       ├── chrome.md
│       ├── claude-code-on-the-web.md
│       ├── cli-reference.md
│       ├── common-workflows.md
│       ├── costs.md
│       ├── data-usage.md
│       ├── desktop.md
│       ├── devcontainer.md
│       ├── discover-plugins.md
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
│       ├── security.md
│       ├── settings.md
│       ├── setup.md
│       ├── skills.md
│       ├── slack.md
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
│       ├── integrations
│       ├── leaderboards
│       ├── logo
│       ├── onboarding
│       ├── reference
│       ├── snippets
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
│       │   ├── endpoints.mdx
│       │   ├── inspector.mdx
│       │   ├── mcp-servers.mdx
│       │   ├── middleware-future.mdx
│       │   ├── middleware.mdx
│       │   └── namespaces.mdx
│       ├── deployment
│       │   └── custom-deployment.mdx
│       ├── development
│       │   ├── architecture.mdx
│       │   ├── contributing.mdx
│       │   └── i18n.mdx
│       ├── integrations
│       │   ├── claude-desktop.mdx
│       │   ├── cursor.mdx
│       │   ├── general-stdio-with-api-key.mdx
│       │   ├── general-stdio-with-oauth.mdx
│       │   ├── open-web-ui.mdx
│       │   └── troubleshooting-future.mdx
│       ├── troubleshooting
│       │   └── oauth-troubleshooting.mdx
│       ├── index.mdx
│       └── quickstart.mdx
├── modelcontextprotocol
│   ├── modelcontextprotocol
│   │   ├── develop
│   │   ├── getting-started
│   │   ├── learn
│   │   ├── tools
│   │   ├── tutorials
│   │   └── sdk.mdx
│   └── python-sdk
│       ├── experimental
│       ├── api.md
│       ├── authorization.md
│       ├── concepts.md
│       ├── index.md
│       ├── installation.md
│       ├── low-level-server.md
│       └── testing.md
├── MoonshotAI
│   ├── kimi-cli
│   │   ├── chat_provider
│   │   ├── contrib
│   │   ├── tooling
│   │   ├── utils
│   │   ├── __init__.py
│   │   ├── __main__.py
│   │   ├── _generate.py
│   │   ├── message.py
│   │   └── py.typed
│   └── kosong
│       ├── chat_provider
│       │   ├── __init__.py
│       │   ├── chaos.py
│       │   ├── echo.py
│       │   ├── kimi.py
│       │   ├── mock.py
│       │   └── openai_common.py
│       ├── contrib
│       │   ├── chat_provider
│       │   │   ├── __init__.py
│       │   │   ├── anthropic.py
│       │   │   ├── common.py
│       │   │   ├── google_genai.py
│       │   │   ├── openai_legacy.py
│       │   │   └── openai_responses.py
│       │   ├── context
│       │   │   ├── __init__.py
│       │   │   └── linear.py
│       │   └── __init__.py
│       ├── tooling
│       │   ├── __init__.py
│       │   ├── empty.py
│       │   ├── error.py
│       │   ├── mcp.py
│       │   └── simple.py
│       ├── utils
│       │   ├── __init__.py
│       │   ├── aio.py
│       │   ├── jsonschema.py
│       │   └── typing.py
│       ├── __init__.py
│       ├── __main__.py
│       ├── _generate.py
│       ├── message.py
│       └── py.typed
├── openai
│   └── codex
│       ├── tui2
│       │   └── performance-testing.md
│       ├── agents_md.md
│       ├── authentication.md
│       ├── CLA.md
│       ├── config.md
│       ├── contributing.md
│       ├── example-config.md
│       ├── exec.md
│       ├── execpolicy.md
│       ├── getting-started.md
│       ├── install.md
│       ├── license.md
│       ├── open-source-fund.md
│       ├── prompts.md
│       ├── sandbox.md
│       ├── skills.md
│       └── slash_commands.md
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
│       │   ├── amp-cli.md
│       │   ├── claude-code.md
│       │   ├── codex.md
│       │   ├── droid.md
│       │   └── gemini-cli.md
│       ├── configuration
│       │   ├── provider
│       │   │   ├── ai-studio.md
│       │   │   ├── antigravity.md
│       │   │   ├── claude-code-compatibility.md
│       │   │   ├── claude-code.md
│       │   │   ├── codex-compatibility.md
│       │   │   ├── codex.md
│       │   │   ├── gemini-cli.md
│       │   │   ├── gemini-compatibility.md
│       │   │   ├── gemini.md
│       │   │   ├── iflow.md
│       │   │   ├── openai-compatibility.md
│       │   │   └── qwen-code.md
│       │   ├── storage
│       │   │   ├── git.md
│       │   │   ├── pgsql.md
│       │   │   └── s3.md
│       │   ├── auth-dir.md
│       │   ├── basic.md
│       │   ├── hot-reloading.md
│       │   ├── options.md
│       │   └── thinking.md
│       ├── docker
│       │   ├── docker-compose.md
│       │   └── docker.md
│       ├── hands-on
│       │   ├── tutorial-0.md
│       │   ├── tutorial-1.md
│       │   ├── tutorial-10.md
│       │   ├── tutorial-11.md
│       │   ├── tutorial-12.md
│       │   ├── tutorial-2.md
│       │   ├── tutorial-3.md
│       │   ├── tutorial-4.md
│       │   ├── tutorial-5.md
│       │   ├── tutorial-6.md
│       │   ├── tutorial-7.md
│       │   ├── tutorial-8.md
│       │   └── tutorial-9.md
│       ├── introduction
│       │   ├── quick-start.md
│       │   └── what-is-cliproxyapi.md
│       ├── management
│       │   ├── api.md
│       │   ├── gui.md
│       │   └── webui.md
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
