from atlassian import Jira

from backlog_automation.config import settings

jira = Jira(
    url=settings.atlassian_url,
    username=settings.atlassian_username,
    password=settings.atlassian_api_token,
    cloud=True,
)


def publish_backlog(epics: list[dict]) -> list[dict]:
    """Create epics, features, and stories in Jira. Returns created issue keys."""
    created = []

    for epic in epics:
        epic_issue = jira.issue_create(
            fields={
                "project": {"key": settings.jira_project_key},
                "summary": epic["title"],
                "description": epic["description"],
                "issuetype": {"name": "Epic"},
            }
        )
        epic_key = epic_issue["key"]
        created.append({"type": "epic", "key": epic_key, "title": epic["title"]})

        for feature in epic.get("features", []):
            feature_issue = jira.issue_create(
                fields={
                    "project": {"key": settings.jira_project_key},
                    "summary": feature["title"],
                    "description": feature["description"],
                    "issuetype": {"name": "Story"},
                    "customfield_10014": epic_key,  # Epic Link
                }
            )
            feature_key = feature_issue["key"]
            created.append({"type": "feature", "key": feature_key, "title": feature["title"]})

            for story in feature.get("stories", []):
                description = (
                    f"*As a* {story['as_a']}\n"
                    f"*I want* {story['i_want']}\n"
                    f"*So that* {story['so_that']}\n\n"
                    f"*Acceptance Criteria:*\n"
                    + "\n".join(f"- {ac}" for ac in story["acceptance_criteria"])
                )
                story_issue = jira.issue_create(
                    fields={
                        "project": {"key": settings.jira_project_key},
                        "summary": story["title"],
                        "description": description,
                        "issuetype": {"name": "Story"},
                        "customfield_10014": epic_key,
                    }
                )
                created.append({"type": "story", "key": story_issue["key"], "title": story["title"]})

    return created
