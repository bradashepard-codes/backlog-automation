# Backlog Automation

## What this project does
Reads Excel and Word documents as foundational context, then uses the Claude API to generate and publish:
- **Jira** — epics, features, and user stories
- **Confluence** — requirements pages and documentation
- **Figma** — annotated wireframe frames and component structure

## Architecture
```
Excel + Word (input)
       │
       ▼
   Claude API  ──► generates structured output
       │
       ├──► Jira  (epics, features, user stories)
       ├──► Confluence  (requirements pages, documentation)
       └──► Figma  (file structure + annotated wireframe frames)
```

## Project structure
```
src/backlog_automation/
├── main.py               # Prefect workflow entry point
├── config.py             # Pydantic settings (reads from .env)
├── readers/
│   ├── excel_reader.py   # Parses Excel input with pandas/openpyxl
│   └── word_reader.py    # Parses Word input with python-docx
├── generators/
│   └── story_generator.py  # Claude API — turns context into structured output
└── publishers/
    ├── jira_publisher.py        # Creates epics/stories via atlassian-python-api
    ├── confluence_publisher.py  # Creates pages via atlassian-python-api
    └── figma_publisher.py       # Creates files/frames via Figma REST API (httpx)
```

## Key constraints
- All secrets (API keys, tokens, URLs) live in `.env` — never hardcoded
- Figma API supports creating files and frames, not generating visual designs — Claude generates the structural spec
- Use Prefect tasks and flows for all orchestration so steps are observable and retryable

## Running locally
```bash
# Install uv if needed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Copy and fill in secrets
cp .env.example .env

# Run the workflow
uv run backlog --input path/to/context.xlsx path/to/brief.docx
```
