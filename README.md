# Documentation References

A curated collection of documentation mirrors with automated semantic search indexing.

<!-- AUTO:MIRROR_STATUS -->
## Mirror Status

| Mirror | Upstream | Branch | Docs Path | Last Commit | Synced At |
| --- | --- | --- | --- | --- | --- |
| Factory-AI/factory | [https://github.com/Factory-AI/factory](https://github.com/Factory-AI/factory) | main | docs | 2b210ba | 2026-02-05T04:51:49Z |
| stanfordnlp/dspy | [https://github.com/stanfordnlp/dspy](https://github.com/stanfordnlp/dspy) | main | docs | 098091f | 2026-02-04T04:44:05Z |
| lastmile-ai/mcp-agent | [https://github.com/lastmile-ai/mcp-agent](https://github.com/lastmile-ai/mcp-agent) | main | docs | f62d849 | 2026-01-26T04:18:33Z |
| MoonshotAI/kimi-cli | [https://github.com/MoonshotAI/kimi-cli](https://github.com/MoonshotAI/kimi-cli) | main | packages/kosong/src/kosong | 1e7e96b | 2026-02-05T04:51:45Z |
| modelcontextprotocol/modelcontextprotocol | [https://github.com/modelcontextprotocol/modelcontextprotocol](https://github.com/modelcontextprotocol/modelcontextprotocol) | main | docs/docs | 94daefd | 2026-02-05T04:51:45Z |
| modelcontextprotocol/python-sdk | [https://github.com/modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk) | main | docs | d3133ae | 2026-02-05T04:51:45Z |
| modelcontextprotocol/go-sdk | [https://github.com/modelcontextprotocol/go-sdk](https://github.com/modelcontextprotocol/go-sdk) | main | docs | 8a39cf6 | 2026-02-04T04:44:05Z |
| ericbuess/claude-code-docs | [https://github.com/ericbuess/claude-code-docs](https://github.com/ericbuess/claude-code-docs) | main | docs | 4c6b5a0 | 2026-02-05T04:51:45Z |
| anthropics/claude-agent-sdk-python | [https://github.com/anthropics/claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python) | main | examples | 7519c96 | 2026-02-04T04:44:05Z |
| browser-use/browser-use | [https://github.com/browser-use/browser-use](https://github.com/browser-use/browser-use) | main | docs | b4a423e | 2026-02-05T04:51:46Z |
| browser-use/workflow-use | [https://github.com/browser-use/workflow-use](https://github.com/browser-use/workflow-use) | main | workflows | 59ec570 | 2026-01-31T04:27:33Z |
| python-trio/trio | [https://github.com/python-trio/trio](https://github.com/python-trio/trio) | main | docs/source | 95d9205 | 2026-02-01T05:04:51Z |
| raycast/extensions | [https://github.com/raycast/extensions](https://github.com/raycast/extensions) | main | docs | 8fd7612 | 2026-02-05T04:51:49Z |
| typst/typst | [https://github.com/typst/typst](https://github.com/typst/typst) | main | docs/reference | 9f83325 | 2026-02-05T04:51:47Z |
<!-- /AUTO:MIRROR_STATUS -->

<!-- AUTO:SEMANTIC_SEARCH -->
## Semantic Search

This repository includes automated indexing for Gemini File Search API.

- **Stores**: 14
- **Files indexed**: 769
- **Total cost**: $0.2402
- **Last sync**: 2026-02-05T04:52:43Z

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
├── ericbuess
│   └── claude-code-docs
│       ├── amazon-bedrock.md
│       ├── analytics.md
│       ├── authentication.md
│       ├── best-practices.md
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
│       ├── features-overview.md
│       ├── github-actions.md
│       ├── gitlab-ci-cd.md
│       ├── google-vertex-ai.md
│       ├── headless.md
│       ├── hooks-guide.md
│       ├── hooks.md
│       ├── how-claude-code-works.md
│       ├── interactive-mode.md
│       ├── jetbrains.md
│       ├── keybindings.md
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
│       ├── permissions.md
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
│       ├── roadmap.mdx
│       └── streaming_guide.md
├── modelcontextprotocol
│   ├── go-sdk
│   │   ├── client.md
│   │   ├── index.html
│   │   ├── protocol.md
│   │   ├── README.md
│   │   ├── rough_edges.md
│   │   ├── server.md
│   │   └── troubleshooting.md
│   ├── modelcontextprotocol
│   │   ├── develop
│   │   ├── extensions
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
│       ├── migration.md
│       └── testing.md
├── MoonshotAI
│   └── kimi-cli
│       ├── chat_provider
│       ├── contrib
│       ├── tooling
│       ├── utils
│       ├── __init__.py
│       ├── __main__.py
│       ├── _generate.py
│       ├── message.py
│       └── py.typed
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
├── typst
│   └── typst
│       ├── export
│       ├── language
│       ├── library
│       ├── groups.yml
│       └── welcome.md
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
