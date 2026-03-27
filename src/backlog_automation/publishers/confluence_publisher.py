from atlassian import Confluence

from backlog_automation.config import settings

confluence = Confluence(
    url=settings.atlassian_url,
    username=settings.atlassian_username,
    password=settings.atlassian_api_token,
    cloud=True,
)


def publish_pages(pages: list[dict]) -> list[dict]:
    """Create Confluence pages. Returns list of created page metadata."""
    created = []

    for page in pages:
        result = confluence.create_page(
            space=settings.confluence_space_key,
            title=page["title"],
            body=page["body"],
        )
        created.append({"title": page["title"], "id": result["id"], "url": result["_links"]["webui"]})

    return created
