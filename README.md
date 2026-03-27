# Backlog Automation

Reads Excel and Word documents as foundational context, then uses the Claude API to generate and publish epics, features, user stories, requirements pages, and wireframe frames across Jira, Confluence, and Figma.

## Architecture

```
Excel + Word (input)
       │
       ▼
   Claude API  ──► generates structured output
       │
       ├──► Jira        (epics, features, user stories)
       ├──► Confluence  (requirements pages, documentation)
       └──► Figma       (file structure + annotated wireframe frames)
```

The workflow is orchestrated with **Prefect**, making each step observable and retryable.

## Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager
- Accounts and API credentials for:
  - [Anthropic](https://console.anthropic.com/)
  - [Atlassian Cloud](https://id.atlassian.com/manage-profile/security/api-tokens) (Jira + Confluence)
  - [Figma](https://www.figma.com/developers/api#access-tokens)

## Setup

```bash
# Install uv if needed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Configure secrets
cp .env.example .env
```

Edit `.env` with your credentials:

| Variable | Description |
|---|---|
| `ANTHROPIC_API_KEY` | Anthropic API key |
| `ATLASSIAN_URL` | Your Atlassian Cloud base URL |
| `ATLASSIAN_USERNAME` | Your Atlassian account email |
| `ATLASSIAN_API_TOKEN` | Atlassian API token |
| `JIRA_PROJECT_KEY` | Target Jira project key |
| `CONFLUENCE_SPACE_KEY` | Target Confluence space key |
| `FIGMA_ACCESS_TOKEN` | Figma personal access token |
| `FIGMA_TEAM_ID` | Figma team ID |

## Usage

```bash
uv run backlog --excel path/to/context.xlsx --word path/to/brief.docx
```

The workflow will print a summary on completion:

```
Jira:       12 issues created
Confluence:  3 pages created
Figma:       5 frames created
```

## Project Structure

```
src/backlog_automation/
├── main.py                        # Prefect flow entry point
├── config.py                      # Pydantic settings (reads .env)
├── readers/
│   ├── excel_reader.py            # Parses Excel input (pandas/openpyxl)
│   └── word_reader.py             # Parses Word input (python-docx)
├── generators/
│   └── story_generator.py         # Claude API — context → structured output
└── publishers/
    ├── jira_publisher.py          # Creates epics/stories (atlassian-python-api)
    ├── confluence_publisher.py    # Creates pages (atlassian-python-api)
    └── figma_publisher.py         # Creates frames (Figma REST API via httpx)
```

## Development

```bash
# Run tests
uv run pytest

# Lint
uv run ruff check .
uv run ruff format .
```
