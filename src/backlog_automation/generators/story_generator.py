import json
import anthropic

from backlog_automation.config import settings

client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

SYSTEM_PROMPT = """You are a senior product manager. Given foundational context from Excel and Word documents,
generate a structured product backlog. Return valid JSON only — no markdown fences, no commentary.

Output schema:
{
  "epics": [
    {
      "title": "string",
      "description": "string",
      "features": [
        {
          "title": "string",
          "description": "string",
          "stories": [
            {
              "title": "string",
              "as_a": "string",
              "i_want": "string",
              "so_that": "string",
              "acceptance_criteria": ["string"]
            }
          ]
        }
      ]
    }
  ],
  "confluence_pages": [
    {
      "title": "string",
      "body": "string (Confluence storage format)"
    }
  ],
  "figma_frames": [
    {
      "name": "string",
      "description": "string",
      "components": ["string"],
      "annotations": ["string"]
    }
  ]
}"""


def generate_backlog(excel_data: dict, word_text: str) -> dict:
    """Send context to Claude and return structured backlog output."""
    user_message = f"""## Excel Data\n{json.dumps(excel_data, indent=2, default=str)}

## Word Document\n{word_text}

Generate the full product backlog from this context."""

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=8096,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )

    return json.loads(response.content[0].text)
