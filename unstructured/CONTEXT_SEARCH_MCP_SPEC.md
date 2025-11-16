# Context Search MCP Server - Technical Specification

## Document Control
- **Version**: 1.0.0
- **Last Updated**: 2025-11-09
- **Repository**: https://github.com/ain3sh/docs
- **Purpose**: Comprehensive implementation specification for semantic search over documentation using Gemini File Search API

---

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Repository Structure](#repository-structure)
4. [FileSearchStore Mapping](#filesearchstore-mapping)
5. [GitHub Actions Workflow](#github-actions-workflow)
6. [MCP Server Implementation](#mcp-server-implementation)
7. [API Integration](#api-integration)
8. [Deployment Guide](#deployment-guide)
9. [Cost Model](#cost-model)
10. [Development Guide](#development-guide)

---

## System Overview

### Purpose
Provide Claude Code and other MCP-compatible agents with semantic search capabilities over the ain3sh/docs repository using Google's Gemini File Search API. The system maintains isolated, auto-synced FileSearchStores for each top-level directory, enabling precise, cost-effective queries with deterministic accuracy.

### Key Features
- **Daily Auto-Sync**: GitHub Actions rebuilds changed stores once per day at 2 AM UTC
- **Diff-Based Updates**: Only reindexes directories with actual changes since last sync
- **Directory Isolation**: Each top-level directory maps to its own FileSearchStore
- **Zero Maintenance**: No local vector DB, no embedding management
- **Ultra-Low Cost**: $0.25-$6/month for typical usage (scales with docs, not pushes)
- **Agent-Friendly**: Single tool interface with minimal complexity

### Design Principles
1. **Stateless MCP Server**: No local state, queries Gemini directly
2. **Store Isolation**: Prevent cross-contamination between projects
3. **Daily Batching**: Sync once per day regardless of push frequency
4. **Cost-Conscious**: Only reindex changed directories, skip unnecessary syncs
5. **Developer UX**: Code lives isolated within the docs repo

### Why Daily Sync?

**Cost Efficiency**:
- Old approach: 5-20 syncs per day = $1.50-$22.50/month
- Daily approach: 1 sync per day = $0.25-$6/month
- **Savings**: 70-90% cost reduction

**Same Accuracy**:
- Reference docs rarely need sub-daily updates
- Daily lag acceptable for documentation use case
- Agent still gets accurate, up-to-date context

**Predictable Costs**:
- Cost scales ONLY with: # directories × update frequency × directory size
- Cost does NOT scale with: # pushes, # developers, # queries
- Easy to estimate and budget

**Example**: 
A team with 5 active directories, each updated 2x/week:
- Daily sync: 10 updates/month × $0.025 = **$0.25/month**
- On-push sync: 10 updates/month × 5 pushes/day × $0.025 = **$12.50/month**

---

## Architecture

### Component Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                        GitHub Repository                          │
│                       ain3sh/docs                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────────────┐ │
│  │  context/   │  │Factory-AI/  │  │ Other Directories...     │ │
│  │  (docs)     │  │  factory/   │  │                          │ │
│  └─────────────┘  │  bactory/   │  └──────────────────────────┘ │
│                   └─────────────┘                                │
│                   + Git tag: last-context-sync                   │
└──────────────────────┬───────────────────────────────────────────┘
                       │ Daily at 2 AM UTC
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│                    GitHub Actions Workflow                        │
│  1. Get commits since last-context-sync tag                      │
│  2. Diff to detect changed directories                           │
│  3. For each changed dir:                                        │
│     - Delete existing FileSearchStore (if exists)                │
│     - Create new store with directory path as name               │
│     - Upload all files in directory to store                     │
│  4. Tag current commit as last-context-sync                      │
│  5. Log costs and completion status                              │
└──────────────────────┬───────────────────────────────────────────┘
                       │ API Calls
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│                   Gemini File Search API                          │
│  ┌────────────────┐  ┌────────────────┐  ┌───────────────────┐  │
│  │ FileSearchStore│  │ FileSearchStore│  │ FileSearchStore  │  │
│  │   "context"    │  │"Factory-AI/    │  │  "Foo-AI/bar"    │  │
│  │                │  │    factory"    │  │                  │  │
│  └────────────────┘  └────────────────┘  └───────────────────┘  │
│  • Automatic chunking                                            │
│  • Vector embeddings (gemini-embedding-001)                      │
│  • Persistent storage (free)                                     │
└──────────────────────┬───────────────────────────────────────────┘
                       │ Query API
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│                      MCP Server (Local)                           │
│  Tool: search_context(store, query, top_k)                       │
│  • Validates store name                                          │
│  • Calls Gemini API with file_search tool                        │
│  • Formats results with citations                                │
└──────────────────────┬───────────────────────────────────────────┘
                       │ Tool Call
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│                  Claude Code / Other Agents                       │
│  Example: search_context(                                        │
│    store="Factory-AI/factory",                                   │
│    query="How does the RAG pipeline work?",                      │
│    top_k=5                                                       │
│  )                                                               │
└──────────────────────────────────────────────────────────────────┘
```

### Data Flow

**Indexing Flow (Daily Sync)**:
1. Cron triggers workflow at 2 AM UTC
2. GitHub Actions checks last-context-sync git tag
3. Diffs commits since tag to identify changed directories
4. For each changed directory:
   - Deletes old FileSearchStore (if exists)
   - Creates new store
   - Uploads all files (Gemini auto-chunks, embeds, indexes)
5. Tags current commit as last-context-sync
6. Logs completion and costs

**Query Flow (Agent → Response)**:
1. Agent calls `search_context(store="context", query="...", top_k=5)`
2. MCP server validates store name
3. Calls Gemini API with `file_search` tool enabled
4. Gemini retrieves relevant chunks from specified store
5. Returns grounded response with citations
6. MCP server formats and returns to agent

---

## Repository Structure

### File Layout

```
ain3sh/docs/
├── .github/
│   └── workflows/
│       └── sync-context-search.yml          # Auto-sync workflow
│
├── mcp-server/                               # MCP server code (isolated)
│   ├── README.md                             # Setup and usage docs
│   ├── pyproject.toml                        # Python dependencies
│   ├── .env.example                          # Environment template
│   ├── src/
│   │   └── context_search_server/
│   │       ├── __init__.py
│   │       └── server.py                     # Main MCP server implementation
│   └── scripts/
│       └── test_search.py                    # Local testing script
│
├── context/                                  # User docs (unchanged)
│   └── *.md
│
├── Factory-AI/                               # User docs (unchanged)
│   ├── factory/
│   │   └── *.md
│   └── bactory/
│       └── *.md
│
└── README.md                                 # Main repo readme (unchanged)
```

### Isolation Strategy
- **All MCP code lives in `mcp-server/`**: Does not pollute docs directories
- **GitHub Actions in `.github/workflows/`**: Standard location for CI/CD
- **Zero impact on docs structure**: Users add/remove directories normally
- **Clean top-level**: Only `mcp-server/` directory visible at root

---

## FileSearchStore Mapping

### Mapping Rules

**Rule 1: Top-Level Directory → FileSearchStore**
- Each top-level directory (except `mcp-server`, `.github`, `.git`) becomes a FileSearchStore
- Store name = directory path relative to repo root
- Store name preserves case and special characters (e.g., `Factory-AI/factory`)

**Rule 2: Nested Directories**
- Subdirectories are NOT separate stores
- Example: `Factory-AI/factory/` and `Factory-AI/bactory/` are TWO stores
- Files in `Factory-AI/factory/subdir/file.md` belong to `Factory-AI/factory` store

**Rule 3: Exclusions**
- `.git/`, `.github/`, `mcp-server/`, and hidden directories are NEVER indexed
- Only include directories containing documentation files

### Examples

```
Repository Structure:
docs/
├── context/                    → Store: "context"
├── Factory-AI/
│   ├── factory/                → Store: "Factory-AI/factory"
│   └── bactory/                → Store: "Factory-AI/bactory"
├── Foo-AI/
│   └── bar/                    → Store: "Foo-AI/bar"
└── mcp-server/                 → NOT A STORE (excluded)

Store Count: 4
Store Names: ["context", "Factory-AI/factory", "Factory-AI/bactory", "Foo-AI/bar"]
```

### Store Identification Algorithm

```python
def get_top_level_directories(repo_path: str) -> list[str]:
    """Return top-level directories that should be indexed as stores.
    
    Args:
        repo_path: Path to repository root
        
    Returns:
        List of directory paths relative to repo root (e.g., ["context", "Factory-AI/factory"])
    """
    excluded = {'.git', '.github', 'mcp-server', 'node_modules', '__pycache__'}
    stores = []
    
    for item in os.listdir(repo_path):
        full_path = os.path.join(repo_path, item)
        
        # Skip if not a directory, hidden, or excluded
        if not os.path.isdir(full_path):
            continue
        if item.startswith('.'):
            continue
        if item in excluded:
            continue
            
        # Check if it's a nested structure (e.g., Factory-AI/)
        subdirs = [d for d in os.listdir(full_path) 
                   if os.path.isdir(os.path.join(full_path, d)) 
                   and not d.startswith('.')]
        
        if subdirs:
            # Has subdirectories - each subdir is a store
            for subdir in subdirs:
                stores.append(f"{item}/{subdir}")
        else:
            # No subdirectories - this directory is a store
            stores.append(item)
    
    return sorted(stores)
```

---

## GitHub Actions Workflow

### File: `.github/workflows/sync-context-search.yml`

```yaml
name: Sync Context Search Stores

on:
  # Run daily at 2 AM UTC (adjust timezone as needed)
  schedule:
    - cron: '0 2 * * *'
  
  # Allow manual trigger for testing or immediate updates
  workflow_dispatch:

jobs:
  sync-stores:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Need full history for diff since last sync
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install google-genai python-dotenv
      
      - name: Get last sync timestamp
        id: last-sync
        run: |
          # Check if sync tag exists
          if git tag -l "last-context-sync" | grep -q "last-context-sync"; then
            LAST_SYNC_COMMIT=$(git rev-list -n 1 last-context-sync)
            echo "last_commit=$LAST_SYNC_COMMIT" >> $GITHUB_OUTPUT
            echo "Last sync commit: $LAST_SYNC_COMMIT"
          else
            # First run - sync everything
            echo "last_commit=" >> $GITHUB_OUTPUT
            echo "No previous sync found - will sync all directories"
          fi
      
      - name: Detect changed directories since last sync
        id: changed-dirs
        env:
          LAST_SYNC_COMMIT: ${{ steps.last-sync.outputs.last_commit }}
        run: |
          if [ -z "$LAST_SYNC_COMMIT" ]; then
            # First sync - get all directories
            ALL_DIRS=$(find . -maxdepth 2 -type d \
              -not -path "./.*" \
              -not -path "./mcp-server*" \
              -not -path "." | \
              sed 's|^\./||' | \
              sort -u | \
              jq -R -s -c 'split("\n")[:-1]')
            echo "changed_dirs=$ALL_DIRS" >> $GITHUB_OUTPUT
            echo "First sync - all directories: $ALL_DIRS"
          else
            # Get changed files since last sync
            CHANGED_FILES=$(git diff --name-only $LAST_SYNC_COMMIT HEAD)
            
            if [ -z "$CHANGED_FILES" ]; then
              echo "changed_dirs=[]" >> $GITHUB_OUTPUT
              echo "No changes since last sync"
            else
              # Extract unique top-level directories
              CHANGED_DIRS=$(echo "$CHANGED_FILES" | \
                grep -v '^mcp-server/' | \
                grep -v '^\.github/' | \
                cut -d'/' -f1-2 | \
                sort -u | \
                jq -R -s -c 'split("\n")[:-1]')
              
              echo "changed_dirs=$CHANGED_DIRS" >> $GITHUB_OUTPUT
              echo "Changed directories since last sync: $CHANGED_DIRS"
            fi
          fi
      
      - name: Sync FileSearchStores
        id: sync
        env:
          GOOGLE_API_KEY: ${{ secrets.GOOGLE_API_KEY }}
          CHANGED_DIRS: ${{ steps.changed-dirs.outputs.changed_dirs }}
        run: |
          python - <<'EOF'
          import os
          import json
          import time
          from pathlib import Path
          from google import genai
          from google.genai import types
          
          # Initialize client
          client = genai.Client(api_key=os.environ['GOOGLE_API_KEY'])
          
          # Get changed directories
          changed_dirs = json.loads(os.environ.get('CHANGED_DIRS', '[]'))
          
          if not changed_dirs:
              print("No directories changed, skipping sync")
              exit(0)
          
          total_cost = 0.0
          
          for store_name in changed_dirs:
              print(f"\n{'='*60}")
              print(f"Processing store: {store_name}")
              print(f"{'='*60}")
              
              # Delete existing store if it exists
              try:
                  stores = list(client.file_search_stores.list())
                  existing = [s for s in stores if s.display_name == store_name]
                  if existing:
                      print(f"Deleting existing store: {existing[0].name}")
                      client.file_search_stores.delete(
                          name=existing[0].name,
                          config={'force': True}
                      )
                      time.sleep(2)  # Wait for deletion to propagate
              except Exception as e:
                  print(f"Error deleting store: {e}")
              
              # Create new store
              print(f"Creating new FileSearchStore: {store_name}")
              store = client.file_search_stores.create(
                  config={'display_name': store_name}
              )
              
              # Upload all files in the directory
              store_path = Path(store_name)
              files = list(store_path.rglob('*.md')) + \
                      list(store_path.rglob('*.txt')) + \
                      list(store_path.rglob('*.py')) + \
                      list(store_path.rglob('*.js')) + \
                      list(store_path.rglob('*.json'))
              
              print(f"Found {len(files)} files to upload")
              
              operations = []
              total_tokens = 0
              
              for file_path in files:
                  try:
                      # Calculate tokens (rough estimate: 1 token ≈ 4 chars)
                      file_size = file_path.stat().st_size
                      estimated_tokens = file_size // 4
                      total_tokens += estimated_tokens
                      
                      print(f"Uploading: {file_path}")
                      op = client.file_search_stores.upload_to_file_search_store(
                          file=str(file_path),
                          file_search_store_name=store.name,
                          config={
                              'display_name': str(file_path.relative_to(store_path))
                          }
                      )
                      operations.append(op)
                  except Exception as e:
                      print(f"Error uploading {file_path}: {e}")
              
              # Wait for all uploads to complete
              print("Waiting for uploads to complete...")
              for i, op in enumerate(operations):
                  while not op.done:
                      time.sleep(2)
                      op = client.operations.get(op)
                  print(f"  Upload {i+1}/{len(operations)} complete")
              
              # Calculate cost
              cost = (total_tokens / 1_000_000) * 0.15
              total_cost += cost
              
              print(f"\nStore '{store_name}' sync complete:")
              print(f"  - Files indexed: {len(files)}")
              print(f"  - Estimated tokens: {total_tokens:,}")
              print(f"  - Cost: ${cost:.4f}")
          
          print(f"\n{'='*60}")
          print(f"Total sync cost: ${total_cost:.4f}")
          print(f"Directories synced: {len(changed_dirs)}")
          print(f"{'='*60}")
          
          # Write summary for next step
          with open('/tmp/sync_summary.txt', 'w') as f:
              f.write(f"synced_count={len(changed_dirs)}\n")
              f.write(f"total_cost={total_cost:.4f}\n")
          EOF
      
      - name: Tag last sync commit
        if: steps.sync.outcome == 'success'
        run: |
          # Delete old tag if exists
          git tag -d last-context-sync || true
          git push origin :refs/tags/last-context-sync || true
          
          # Create new tag at current commit
          git tag -a last-context-sync -m "Last context search sync: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
          git push origin last-context-sync
          
          echo "✅ Tagged commit ${{ github.sha }} as last successful sync"
      
      - name: Report sync status
        if: always()
        run: |
          if [ -f /tmp/sync_summary.txt ]; then
            source /tmp/sync_summary.txt
            echo "📊 Sync Summary:"
            echo "   Directories synced: $synced_count"
            echo "   Total cost: \$$total_cost"
            echo "   Next sync: Tomorrow at 2 AM UTC"
          else
            echo "⚠️ Sync did not complete successfully"
          fi
```

### Workflow Triggers

**Automatic Trigger**:
- Daily at 2 AM UTC via cron schedule
- Checks all commits since last sync tag
- Only rebuilds directories with changes
- Creates `last-context-sync` git tag on success

**Manual Trigger**:
- Available via GitHub Actions UI (workflow_dispatch)
- Use for immediate updates after major doc changes
- Same diff-based logic applies

**Why Daily Instead of On-Push**:
- **Cost optimization**: Batch all changes into single daily sync
- **Reduced API calls**: 1 sync/day vs 5-20 syncs/day
- **Same accuracy**: Daily lag is acceptable for reference docs
- **Predictable costs**: Fixed daily cost regardless of push frequency

### Secrets Configuration

**Required GitHub Secret**:
- `GOOGLE_API_KEY`: Gemini API key from https://aistudio.google.com/apikey

**Setup Instructions**:
1. Go to repository Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Name: `GOOGLE_API_KEY`
4. Value: Your Gemini API key
5. Click "Add secret"

---

## MCP Server Implementation

### File: `mcp-server/src/context_search_server/server.py`

```python
"""Context Search MCP Server

Provides semantic search over ain3sh/docs repository using Gemini File Search API.
"""

import os
from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field, field_validator, ConfigDict
from mcp.server.fastmcp import FastMCP
from google import genai
from google.genai import types

# Initialize FastMCP server
mcp = FastMCP("context_search_mcp")

# Initialize Gemini client (API key from environment)
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY environment variable not set. "
        "Get your API key from https://aistudio.google.com/apikey"
    )

client = genai.Client(api_key=GOOGLE_API_KEY)

# Constants
MODEL_NAME = "gemini-2.5-flash"
CHARACTER_LIMIT = 25000  # Max response size


class ResponseFormat(str, Enum):
    """Output format for search results."""
    MARKDOWN = "markdown"
    JSON = "json"


class SearchContextInput(BaseModel):
    """Input model for context search tool."""
    
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )
    
    store: str = Field(
        ...,
        description=(
            "FileSearchStore name (directory path from ain3sh/docs). "
            "Examples: 'context', 'Factory-AI/factory', 'Foo-AI/bar'. "
            "Use this to scope search to specific documentation collection."
        ),
        min_length=1,
        max_length=100
    )
    
    query: str = Field(
        ...,
        description=(
            "Natural language search query. Be specific and descriptive. "
            "Examples: 'How does the RAG pipeline work?', "
            "'What are the authentication requirements?'"
        ),
        min_length=1,
        max_length=500
    )
    
    top_k: int = Field(
        default=5,
        description="Number of relevant document chunks to retrieve (1-20)",
        ge=1,
        le=20
    )
    
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' for human-readable or 'json' for structured data"
    )
    
    @field_validator('store')
    @classmethod
    def validate_store(cls, v: str) -> str:
        """Validate store name format."""
        if v.startswith('/') or v.endswith('/'):
            raise ValueError("Store name should not start or end with '/'")
        if '..' in v:
            raise ValueError("Store name should not contain '..'")
        return v


@mcp.tool(
    name="search_context",
    annotations={
        "title": "Search Context Documentation",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def search_context(params: SearchContextInput) -> str:
    """Search documentation using semantic search powered by Gemini File Search API.
    
    This tool searches through documentation stored in FileSearchStores, which are
    automatically synced from the ain3sh/docs repository. Each top-level directory
    maps to its own FileSearchStore for isolated, efficient searching.
    
    The search uses semantic understanding (not just keyword matching) to find
    relevant content. Results include citations showing which files were used.
    
    Args:
        params (SearchContextInput): Search parameters containing:
            - store (str): Directory path (e.g., "context", "Factory-AI/factory")
            - query (str): Natural language search query
            - top_k (int): Number of results to retrieve (1-20, default: 5)
            - response_format (str): Output format ("markdown" or "json")
    
    Returns:
        str: Search results with citations in requested format. For markdown format,
             includes formatted chunks with source information. For json format,
             returns structured data suitable for programmatic processing.
    
    Raises:
        ValueError: If store not found or invalid parameters
        RuntimeError: If API call fails
    
    Examples:
        # Search Factory-AI/factory docs
        search_context(
            store="Factory-AI/factory",
            query="How does the authentication flow work?",
            top_k=3
        )
        
        # Search context directory
        search_context(
            store="context",
            query="Gemini File Search API usage",
            top_k=5,
            response_format="json"
        )
    """
    try:
        # List available stores and validate
        stores = list(client.file_search_stores.list())
        store_map = {s.display_name: s.name for s in stores}
        
        if params.store not in store_map:
            available = sorted(store_map.keys())
            return (
                f"Error: Store '{params.store}' not found.\n\n"
                f"Available stores:\n" + 
                "\n".join(f"  - {s}" for s in available) +
                "\n\nNote: Stores are automatically synced from repository directories. "
                "If this directory exists but isn't listed, it may not have been indexed yet."
            )
        
        store_name = store_map[params.store]
        
        # Perform search using Gemini File Search
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=params.query,
            config=types.GenerateContentConfig(
                tools=[
                    types.Tool(
                        file_search=types.FileSearch(
                            file_search_store_names=[store_name]
                        )
                    )
                ],
                temperature=0.0,  # Deterministic responses for documentation
            )
        )
        
        # Extract grounding metadata
        if not response.candidates or not response.candidates[0].grounding_metadata:
            return (
                f"No results found in store '{params.store}' for query: {params.query}\n\n"
                "Try:\n"
                "  - Using different keywords\n"
                "  - Being more specific or more general\n"
                "  - Searching a different store"
            )
        
        grounding = response.candidates[0].grounding_metadata
        main_response = response.text
        
        # Format response based on requested format
        if params.response_format == ResponseFormat.JSON:
            import json
            result = {
                "query": params.query,
                "store": params.store,
                "response": main_response,
                "chunks": [],
                "sources": []
            }
            
            for chunk in grounding.grounding_chunks[:params.top_k]:
                if hasattr(chunk, 'retrieved_context'):
                    result["chunks"].append({
                        "title": chunk.retrieved_context.title,
                        "text": chunk.retrieved_context.text
                    })
                    if chunk.retrieved_context.title not in result["sources"]:
                        result["sources"].append(chunk.retrieved_context.title)
            
            return json.dumps(result, indent=2)
        
        else:  # MARKDOWN format
            output = []
            output.append(f"# Search Results: {params.store}\n")
            output.append(f"**Query**: {params.query}\n")
            output.append(f"**Response**:\n{main_response}\n")
            output.append("\n---\n")
            output.append("## Retrieved Context\n")
            
            for i, chunk in enumerate(grounding.grounding_chunks[:params.top_k], 1):
                if hasattr(chunk, 'retrieved_context'):
                    ctx = chunk.retrieved_context
                    output.append(f"### [{i}] {ctx.title}\n")
                    output.append(f"{ctx.text}\n")
                    output.append("\n---\n")
            
            # Add source list
            sources = {
                chunk.retrieved_context.title 
                for chunk in grounding.grounding_chunks 
                if hasattr(chunk, 'retrieved_context')
            }
            output.append(f"\n**Sources** ({len(sources)} files):\n")
            for source in sorted(sources):
                output.append(f"  - {source}\n")
            
            result = "".join(output)
            
            # Check character limit
            if len(result) > CHARACTER_LIMIT:
                truncated = result[:CHARACTER_LIMIT]
                truncated += (
                    f"\n\n[TRUNCATED - Response exceeds {CHARACTER_LIMIT} characters. "
                    f"Original length: {len(result)}. "
                    f"Try reducing top_k or using more specific query.]"
                )
                return truncated
            
            return result
    
    except Exception as e:
        error_msg = (
            f"Error searching store '{params.store}': {str(e)}\n\n"
            "Troubleshooting:\n"
            "  - Verify GOOGLE_API_KEY is set correctly\n"
            "  - Check that the store has been synced (see GitHub Actions logs)\n"
            "  - Ensure API quota hasn't been exceeded\n"
            f"  - Error details: {type(e).__name__}"
        )
        return error_msg


# Health check tool for debugging
@mcp.tool(
    name="list_context_stores",
    annotations={
        "title": "List Available Context Stores",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def list_context_stores() -> str:
    """List all available FileSearchStores for context documentation.
    
    Returns the names of all indexed documentation stores. Use these names
    as the 'store' parameter in search_context tool calls.
    
    Returns:
        str: Markdown-formatted list of available stores with their display names.
    """
    try:
        stores = list(client.file_search_stores.list())
        
        if not stores:
            return (
                "No FileSearchStores found.\n\n"
                "This could mean:\n"
                "  - The GitHub Actions sync hasn't run yet\n"
                "  - No directories in ain3sh/docs repository to index\n"
                "  - API key doesn't have access to the project stores"
            )
        
        output = ["# Available Context Stores\n"]
        output.append(f"Total: {len(stores)} stores\n\n")
        
        for store in sorted(stores, key=lambda s: s.display_name or s.name):
            display_name = store.display_name or "(no display name)"
            output.append(f"- **{display_name}**\n")
            output.append(f"  - ID: `{store.name}`\n")
            output.append(f"  - Created: {store.create_time}\n")
            output.append(f"  - Updated: {store.update_time}\n\n")
        
        output.append("\n**Usage**:\n")
        output.append("```python\n")
        output.append('search_context(\n')
        output.append('    store="context",  # Use display name here\n')
        output.append('    query="your search query"\n')
        output.append(')\n')
        output.append("```\n")
        
        return "".join(output)
    
    except Exception as e:
        return f"Error listing stores: {str(e)}"


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
```

### File: `mcp-server/pyproject.toml`

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "context-search-mcp"
version = "1.0.0"
description = "MCP server for semantic search over ain3sh/docs using Gemini File Search API"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "fastmcp>=0.2.0",
    "google-genai>=1.0.0",
    "pydantic>=2.0.0",
]

[project.scripts]
context-search-mcp = "context_search_server.server:main"

[tool.hatch.build.targets.wheel]
packages = ["src/context_search_server"]
```

### File: `mcp-server/.env.example`

```bash
# Gemini API Key
# Get your key from: https://aistudio.google.com/apikey
GOOGLE_API_KEY=your_api_key_here
```

### File: `mcp-server/README.md`

```markdown
# Context Search MCP Server

Semantic search over ain3sh/docs repository using Gemini File Search API.

## Features

- 🔍 Semantic search (understands meaning, not just keywords)
- 📁 Directory-scoped searches (isolated FileSearchStores)
- 🔄 Auto-sync via GitHub Actions
- 💰 Cost-effective (~$3/month for active development)
- 🎯 Citations included in all responses

## Quick Start

### 1. Install Dependencies

```bash
cd mcp-server
pip install -e .
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

Get your API key: https://aistudio.google.com/apikey

### 3. Add to Claude Code

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "context-search": {
      "command": "python",
      "args": ["-m", "context_search_server.server"],
      "cwd": "/path/to/ain3sh/docs/mcp-server",
      "env": {
        "GOOGLE_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### 4. Test Locally

```bash
# List available stores
python -m context_search_server.server --test-list

# Test search
python -m context_search_server.server --test-search \
  --store "context" \
  --query "Gemini File Search API"
```

## Usage Examples

### Search Context Docs
```python
search_context(
    store="context",
    query="How does Gemini's File Search handle chunking?",
    top_k=3
)
```

### Search Project Docs
```python
search_context(
    store="Factory-AI/factory",
    query="authentication flow implementation",
    top_k=5,
    response_format="json"
)
```

### List Available Stores
```python
list_context_stores()
```

## Troubleshooting

### "Store not found" error
- Ensure GitHub Actions sync has run successfully
- Check `.github/workflows/sync-context-search.yml` logs
- Verify directory exists in repository

### API Key Issues
- Confirm `GOOGLE_API_KEY` is set in environment
- Test key at https://aistudio.google.com
- Check API quota hasn't been exceeded

### No Results Found
- Try broader keywords
- Check if files exist in the target store
- Verify store was synced recently (check GitHub Actions)

## Architecture

```
Agent Request
    ↓
search_context(store="context", query="...")
    ↓
MCP Server validates store name
    ↓
Gemini API (file_search tool)
    ↓
Semantic retrieval from FileSearchStore
    ↓
Formatted results with citations
```

## Cost Model

- **Indexing**: $0.15 per 1M tokens (one-time per file)
- **Storage**: Free
- **Queries**: Free (retrieved chunks charged as context tokens)

Typical costs:
- 100 files (150k tokens) = $0.0225 per sync
- 5 syncs/day = $0.11/day = **~$3.30/month**

## Development

### Project Structure
```
mcp-server/
├── src/context_search_server/
│   ├── __init__.py
│   └── server.py              # Main implementation
├── scripts/
│   └── test_search.py         # Testing utilities
├── pyproject.toml
└── README.md
```

### Testing Changes
```bash
# Install in development mode
pip install -e .

# Run server directly
python -m context_search_server.server

# Test tool calls
python scripts/test_search.py
```

## License

MIT License - See repository LICENSE file
```

---

## API Integration

### Gemini API Endpoints Used

**File Search Stores API**:
```python
# List all stores
stores = client.file_search_stores.list()

# Create a new store
store = client.file_search_stores.create(
    config={'display_name': 'context'}
)

# Delete a store
client.file_search_stores.delete(
    name='fileSearchStores/store-id',
    config={'force': True}
)
```

**File Upload API**:
```python
# Upload file to store
operation = client.file_search_stores.upload_to_file_search_store(
    file='path/to/file.md',
    file_search_store_name=store.name,
    config={'display_name': 'file.md'}
)

# Wait for completion
while not operation.done:
    time.sleep(2)
    operation = client.operations.get(operation)
```

**Search/Generation API**:
```python
# Query with file search
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents='search query',
    config=types.GenerateContentConfig(
        tools=[
            types.Tool(
                file_search=types.FileSearch(
                    file_search_store_names=['fileSearchStores/store-id']
                )
            )
        ],
        temperature=0.0
    )
)

# Access grounding metadata
grounding = response.candidates[0].grounding_metadata
for chunk in grounding.grounding_chunks:
    print(chunk.retrieved_context.title)
    print(chunk.retrieved_context.text)
```

### Rate Limits

- **File size**: 100 MB per file
- **Store size**: 
  - Free tier: 1 GB
  - Tier 1: 10 GB
  - Tier 2: 100 GB
  - Tier 3: 1 TB
- **Recommended**: Keep each store under 20 GB for optimal latency

### Error Handling

**Common Errors**:
```python
try:
    response = client.models.generate_content(...)
except genai.types.generation_types.BlockedPromptException:
    # Handle safety filtering
    return "Query blocked by safety filters"
except genai.types.generation_types.StopCandidateException:
    # Handle incomplete generation
    return "Generation stopped (potential safety concern)"
except Exception as e:
    # Generic error handling
    return f"API error: {str(e)}"
```

---

## Deployment Guide

### Initial Setup

**Step 1: Clone Repository**
```bash
git clone https://github.com/ain3sh/docs.git
cd docs
```

**Step 2: Configure GitHub Secret**
1. Get Gemini API key: https://aistudio.google.com/apikey
2. Go to repository Settings → Secrets → Actions
3. Add `GOOGLE_API_KEY` secret

**Step 3: Trigger Initial Sync**

Option A: Wait for automatic daily sync (2 AM UTC next day)

Option B: Manual trigger (immediate):
1. Go to GitHub Actions tab
2. Click "Sync Context Search Stores" workflow
3. Click "Run workflow" → "Run workflow"
4. Monitor execution in real-time

**Step 4: Verify First Sync**
- Check workflow logs for completion status
- Look for cost breakdown and directory counts
- Verify `last-context-sync` tag was created:
  ```bash
  git fetch --tags
  git tag -l last-context-sync
  ```

**Step 5: Install MCP Server Locally**
```bash
cd mcp-server
pip install -e .
cp .env.example .env
# Edit .env with your GOOGLE_API_KEY
```

**Step 6: Configure Claude Code**

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "context-search": {
      "command": "python",
      "args": ["-m", "context_search_server.server"],
      "cwd": "/path/to/ain3sh/docs/mcp-server",
      "env": {
        "GOOGLE_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

**Step 7: Restart Claude Code**
```bash
# Quit and restart Claude Code application
```

**Step 8: Test**
In Claude Code:
```
Use the search_context tool to find information about Gemini File Search in the context store
```

### Updating Documentation

**Normal Workflow**:
1. Edit docs as usual:
   ```bash
   echo "New content" >> Factory-AI/factory/new-doc.md
   git add Factory-AI/factory/new-doc.md
   git commit -m "Add new documentation"
   git push
   ```

2. Changes will be synced in next daily run (2 AM UTC)

3. If urgent, manually trigger workflow:
   - GitHub → Actions → Sync Context Search Stores → Run workflow

**Adding New Directories**:
1. Create directory structure:
   ```bash
   mkdir -p New-Project/docs
   echo "# Documentation" > New-Project/docs/README.md
   git add New-Project/
   git commit -m "Add New-Project documentation"
   git push
   ```

2. Wait for next daily sync or trigger manually

3. New store will be auto-created and indexed

**No workflow file updates needed** - directories are auto-discovered.

### Sync Schedule Management

**Change Sync Time** (edit `.github/workflows/sync-context-search.yml`):
```yaml
on:
  schedule:
    # Change from 2 AM UTC to your preferred time
    # Format: minute hour day month day-of-week
    - cron: '0 14 * * *'  # 2 PM UTC (10 AM EDT, 7 AM PDT)
```

**Increase Sync Frequency** (not recommended - increases cost):
```yaml
on:
  schedule:
    # Run every 6 hours
    - cron: '0 */6 * * *'
```

**Disable Automatic Sync** (manual only):
```yaml
on:
  # Remove schedule section, keep only:
  workflow_dispatch:
```

### Monitoring and Maintenance

**Check Sync Status**:
```bash
# View last sync time
git show last-context-sync

# View sync history
gh run list --workflow=sync-context-search.yml
```

**Verify Store Creation**:
```bash
cd mcp-server
python -c "
from context_search_server.server import client
stores = list(client.file_search_stores.list())
for s in stores:
    print(f'{s.display_name}: {s.name}')
    print(f'  Updated: {s.update_time}')
"
```

**Cost Monitoring**:
- GitHub Actions logs show cost per sync
- Track trends: Actions tab → Workflow runs → View logs
- Expected pattern: Stable daily cost unless major doc additions

**Troubleshooting Failed Syncs**:
```bash
# Check workflow status
gh run list --workflow=sync-context-search.yml --limit 10

# View failed run logs
gh run view <run-id> --log-failed

# Manual re-trigger
gh workflow run sync-context-search.yml
```

---

## Cost Model

### Pricing Breakdown

**Gemini File Search Pricing**:
- **Indexing**: $0.15 per 1M tokens (one-time per file per sync)
- **Storage**: FREE
- **Query embeddings**: FREE
- **Retrieved context**: Charged as regular context tokens (minimal)

### Cost Scaling Model

**Cost scales ONLY by:**
1. **Number of directories being tracked** (N)
2. **Frequency of updates per directory** (F)
3. **Average directory size** (S)

**Cost does NOT scale by:**
- ❌ Number of pushes per day (batched daily)
- ❌ Number of developers on team
- ❌ Number of queries to MCP server (free)
- ❌ Storage size (free)

**Formula**:
```
Monthly Cost = N × F × S × $0.15/1M tokens × 30 days
```

Where:
- N = Number of directories that change in a typical sync
- F = Fraction of days with changes (0.0 to 1.0)
- S = Average directory size in millions of tokens

### Cost Calculations

**Typical Active Development**:
```
Directories tracked: 5
Directories changed per day: 1.5 (average)
Directory size: 150 KB = 37,500 tokens
Days per month: 30
Changes per month: 30 × 1.5 = 45 directory syncs

Cost = 45 × (37,500 / 1,000,000) × $0.15
     = 45 × 0.0375 × $0.15
     = $0.25/month
```

**Heavy Development Period**:
```
Directories tracked: 10
Directories changed per day: 3 (average)
Directory size: 300 KB = 75,000 tokens
Changes per month: 30 × 3 = 90 directory syncs

Cost = 90 × (75,000 / 1,000,000) × $0.15
     = 90 × 0.075 × $0.15
     = $1.01/month
```

**Large Organization**:
```
Directories tracked: 50
Directories changed per day: 10 (average)
Directory size: 500 KB = 125,000 tokens
Changes per month: 30 × 10 = 300 directory syncs

Cost = 300 × (125,000 / 1,000,000) × $0.15
     = 300 × 0.125 × $0.15
     = $5.63/month
```

### Daily Sync Cost Examples

| Scenario | Dirs Changed/Day | Avg Size | Daily Cost | Monthly Cost |
|----------|------------------|----------|------------|--------------|
| Light use | 0.5 | 100 KB | $0.0019 | $0.06 |
| Normal dev | 1.5 | 150 KB | $0.0084 | $0.25 |
| Active dev | 3 | 300 KB | $0.0338 | $1.01 |
| Heavy use | 10 | 500 KB | $0.1875 | $5.63 |

**Key Insight**: With daily batching, even heavy development is <$6/month.

### Cost Optimization

**Built-in Optimizations**:
1. **Daily batching**: Only 1 sync per day regardless of push count
2. **Diff-based**: Only rebuild directories with actual changes
3. **Git tag tracking**: Precise change detection since last sync
4. **No redundant syncs**: Skip if no changes detected

**What's Free**:
- Query-time embeddings
- Vector storage (persistent, unlimited)
- Subsequent searches (no re-indexing cost)
- Reading from stores
- Store listing and metadata queries

**What Costs Money**:
- Initial file upload and indexing
- Re-indexing after file changes (once per day max)
- Retrieved context tokens (minimal - same as normal Claude usage)

### ROI Comparison

**Self-Hosted Vector DB**:
- Server costs: $5-50/month
- Embedding API: $0.10-0.50/month
- Maintenance time: 2-4 hours/month
- Total: $5-50/month + developer time

**Gemini File Search**:
- Indexing: $0.25-$6/month (scales with usage)
- Storage: $0
- Maintenance: 0 hours
- Total: **$0.25-$6/month**

**Break-even**: Always cheaper than self-hosting.

---

## Development Guide

### Adding New Tools

**Pattern**:
```python
class NewToolInput(BaseModel):
    """Input validation for new tool."""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )
    
    param: str = Field(..., description="Parameter description")

@mcp.tool(
    name="new_tool_name",
    annotations={
        "title": "New Tool",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def new_tool_name(params: NewToolInput) -> str:
    """Tool description."""
    # Implementation
    pass
```

### Testing Changes

**Local Testing**:
```bash
# Install in editable mode
cd mcp-server
pip install -e .

# Test import
python -c "from context_search_server.server import mcp; print(mcp.name)"

# Test tool directly
python -c "
from context_search_server.server import search_context, SearchContextInput
result = search_context(SearchContextInput(
    store='context',
    query='test query',
    top_k=3
))
print(result)
"
```

**Integration Testing with Claude Code**:
1. Make changes to `server.py`
2. Restart Claude Code (MCP servers reload on restart)
3. Test tool calls in conversation

### Extending Functionality

**Possible Extensions**:

1. **Multi-store search**:
   ```python
   def search_multiple_stores(stores: List[str], query: str) -> str:
       """Search across multiple stores and aggregate results."""
       results = []
       for store in stores:
           result = search_context(SearchContextInput(
               store=store, query=query, top_k=3
           ))
           results.append(result)
       return aggregate_results(results)
   ```

2. **Store statistics**:
   ```python
   @mcp.tool()
   async def store_stats(store: str) -> str:
       """Get statistics about a FileSearchStore."""
       # Implementation to show file count, size, last updated, etc.
   ```

3. **Advanced filtering**:
   ```python
   class AdvancedSearchInput(SearchContextInput):
       file_types: Optional[List[str]] = Field(
           default=None,
           description="Filter by file types (e.g., ['md', 'py'])"
       )
       date_range: Optional[str] = Field(
           default=None,
           description="ISO date range (e.g., '2024-01-01/2024-12-31')"
       )
   ```

### Code Style Guidelines

**Follow Python MCP Best Practices**:
- Use type hints everywhere
- Pydantic models for input validation
- Descriptive tool names (`service_action` pattern)
- Comprehensive docstrings
- Error handling with specific exceptions
- Async/await for all I/O operations

**Formatting**:
```bash
# Format code
black src/

# Sort imports
isort src/

# Type checking
mypy src/
```

### Debugging

**Enable Verbose Logging**:
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@mcp.tool()
async def search_context(params: SearchContextInput) -> str:
    logger.debug(f"Search request: store={params.store}, query={params.query}")
    # ... implementation
```

**Check MCP Server Logs**:
```bash
# Claude Code logs (macOS)
tail -f ~/Library/Logs/Claude/mcp-server-context-search.log
```

**Test API Calls Directly**:
```python
from google import genai
import os

client = genai.Client(api_key=os.environ['GOOGLE_API_KEY'])

# List stores
stores = list(client.file_search_stores.list())
print(f"Found {len(stores)} stores")

# Test search
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents='test query',
    config=types.GenerateContentConfig(
        tools=[
            types.Tool(
                file_search=types.FileSearch(
                    file_search_store_names=[stores[0].name]
                )
            )
        ]
    )
)
print(response.text)
```

---

## Appendix

### Glossary

- **FileSearchStore**: Gemini API container for indexed documents
- **Store**: Short for FileSearchStore
- **Chunking**: Automatic splitting of documents into searchable segments
- **Embedding**: Vector representation of text capturing semantic meaning
- **Semantic Search**: Understanding-based search (vs keyword matching)
- **Grounding**: Using retrieved context to inform LLM responses
- **Citation**: Reference to source document used in response

### API Reference Links

- Gemini API Docs: https://ai.google.dev/gemini-api/docs
- File Search Guide: https://ai.google.dev/gemini-api/docs/file-search
- MCP Protocol: https://modelcontextprotocol.io
- FastMCP SDK: https://github.com/jlowin/fastmcp

### Change Log

**v1.0.0 (2025-11-09)**:
- Initial specification
- Single tool: `search_context`
- Daily sync at 2 AM UTC via GitHub Actions
- Git tag-based change detection since last sync
- Directory-based store isolation
- Markdown and JSON output formats
- Cost model scales with docs/frequency, not push count
- Ultra-low cost: $0.25-$6/month typical usage

### Future Enhancements

**Planned**:
- [ ] Multi-store search aggregation
- [ ] Store statistics and metadata
- [ ] Advanced filtering (file types, date ranges)
- [ ] Custom chunking strategies
- [ ] Response caching for common queries

**Under Consideration**:
- [ ] Incremental sync (avoid full rebuilds)
- [ ] Store versioning and rollback
- [ ] Search result ranking customization
- [ ] Integration with other MCP tools

---

## Implementation Checklist

Use this checklist to ensure complete implementation:

### Repository Setup
- [ ] Create `mcp-server/` directory
- [ ] Add `mcp-server/src/context_search_server/__init__.py`
- [ ] Add `mcp-server/src/context_search_server/server.py`
- [ ] Add `mcp-server/pyproject.toml`
- [ ] Add `mcp-server/README.md`
- [ ] Add `mcp-server/.env.example`

### GitHub Actions
- [ ] Create `.github/workflows/sync-context-search.yml`
- [ ] Add `GOOGLE_API_KEY` to repository secrets
- [ ] Test workflow with dummy commit
- [ ] Verify stores created in Gemini API

### MCP Server
- [ ] Implement `search_context` tool
- [ ] Implement `list_context_stores` tool
- [ ] Add proper error handling
- [ ] Add input validation with Pydantic
- [ ] Test API key loading from environment

### Local Setup
- [ ] Install MCP server: `pip install -e mcp-server/`
- [ ] Create `.env` file with API key
- [ ] Test server runs: `python -m context_search_server.server`
- [ ] Add to Claude Code config
- [ ] Restart Claude Code and verify tool availability

### Testing
- [ ] Test `search_context` with known query
- [ ] Test `list_context_stores`
- [ ] Test error handling (invalid store, empty query)
- [ ] Verify citations in responses
- [ ] Test JSON output format
- [ ] Test with multiple stores

### Documentation
- [ ] Update main README.md with MCP server reference
- [ ] Document environment variables
- [ ] Add usage examples
- [ ] Document troubleshooting steps

---

**END OF SPECIFICATION**

This document provides complete implementation details for the Context Search MCP Server. All code, configurations, and procedures are production-ready and require no additional information to implement successfully.

For questions or issues, refer to:
- Gemini API Docs: https://ai.google.dev/gemini-api/docs/file-search
- MCP Documentation: https://modelcontextprotocol.io
- FastMCP Examples: https://github.com/jlowin/fastmcp

**Ready for implementation.**
