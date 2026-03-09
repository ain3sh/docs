# Documentation References

A curated collection of documentation mirrors with automated semantic search indexing.

<!-- AUTO:MIRROR_STATUS -->
## Mirror Status

| Mirror | Upstream | Branch | Docs Path | Last Commit | Synced At |
| --- | --- | --- | --- | --- | --- |
| Factory-AI/factory | [https://github.com/Factory-AI/factory](https://github.com/Factory-AI/factory) | main | docs | e6995b2 | 2026-03-07T04:24:27Z |
| vadimdemedes/ink | [https://github.com/vadimdemedes/ink](https://github.com/vadimdemedes/ink) | master | src | a27a17e | 2026-03-09T08:03:23Z |
| stanfordnlp/dspy | [https://github.com/stanfordnlp/dspy](https://github.com/stanfordnlp/dspy) | main | docs | 43bf2c5 | 2026-03-07T04:24:23Z |
| lastmile-ai/mcp-agent | [https://github.com/lastmile-ai/mcp-agent](https://github.com/lastmile-ai/mcp-agent) | main | docs | f62d849 | 2026-01-26T04:18:33Z |
| MoonshotAI/kimi-cli | [https://github.com/MoonshotAI/kimi-cli](https://github.com/MoonshotAI/kimi-cli) | main | packages/kosong/src/kosong | 0a92cf6 | 2026-03-09T08:03:23Z |
| modelcontextprotocol/modelcontextprotocol | [https://github.com/modelcontextprotocol/modelcontextprotocol](https://github.com/modelcontextprotocol/modelcontextprotocol) | main | docs/docs | 8e2634d | 2026-03-07T04:24:22Z |
| modelcontextprotocol/python-sdk | [https://github.com/modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk) | main | docs | 7ba41dc | 2026-03-07T04:24:22Z |
| anthropics/claude-agent-sdk-python | [https://github.com/anthropics/claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python) | main | examples | d6f0352 | 2026-03-07T04:24:23Z |
| browser-use/browser-use | [https://github.com/browser-use/browser-use](https://github.com/browser-use/browser-use) | main | docs | 9b103bb | 2026-03-08T04:46:51Z |
| browser-use/workflow-use | [https://github.com/browser-use/workflow-use](https://github.com/browser-use/workflow-use) | main | workflows | 59ec570 | 2026-01-31T04:27:33Z |
| python-trio/trio | [https://github.com/python-trio/trio](https://github.com/python-trio/trio) | main | docs/source | 3dd35d7 | 2026-03-01T04:57:52Z |
| raycast/extensions | [https://github.com/raycast/extensions](https://github.com/raycast/extensions) | main | docs | 8285828 | 2026-03-09T08:03:26Z |
| typst/typst | [https://github.com/typst/typst](https://github.com/typst/typst) | main | docs/reference | 364ece3 | 2026-03-06T04:45:21Z |
<!-- /AUTO:MIRROR_STATUS -->

<!-- AUTO:SEMANTIC_SEARCH -->
## Semantic Search

This repository includes automated indexing for Gemini File Search API.

- **Stores**: 13
- **Files indexed**: 872
- **Total cost**: $0.2546
- **Last sync**: 2026-03-09T08:04:10Z

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
│   │   ├── legacy
│   │   ├── logo
│   │   ├── cloud.mdx
│   │   ├── development.mdx
│   │   ├── docs.json
│   │   ├── favicon.ico
│   │   ├── favicon.svg
│   │   ├── introduction.mdx
│   │   ├── quickstart.mdx
│   │   ├── quickstart_llm.mdx
│   │   ├── README.md
│   │   ├── supported-models.mdx
│   │   └── use-cloud.mdx
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
├── Factory-AI
│   └── factory
│       ├── changelog
│       ├── cli
│       ├── enterprise
│       ├── guides
│       ├── images
│       ├── integrations
│       ├── jp
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
│       ├── style.css
│       └── support.mdx
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
├── vadimdemedes
│   └── ink
│       ├── components
│       ├── hooks
│       ├── ansi-tokenizer.ts
│       ├── colorize.ts
│       ├── cursor-helpers.ts
│       ├── devtools-window-polyfill.ts
│       ├── devtools.ts
│       ├── dom.ts
│       ├── get-max-width.ts
│       ├── global.d.ts
│       ├── index.ts
│       ├── ink.tsx
│       ├── input-parser.ts
│       ├── instances.ts
│       ├── kitty-keyboard.ts
│       ├── log-update.ts
│       ├── measure-element.ts
│       ├── measure-text.ts
│       ├── output.ts
│       ├── parse-keypress.ts
│       ├── reconciler.ts
│       ├── render-background.ts
│       ├── render-border.ts
│       ├── render-node-to-output.ts
│       ├── render-to-string.ts
│       ├── render.ts
│       ├── renderer.ts
│       ├── sanitize-ansi.ts
│       ├── squash-text-nodes.ts
│       ├── styles.ts
│       ├── utils.ts
│       ├── wrap-text.ts
│       └── write-synchronized.ts
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
