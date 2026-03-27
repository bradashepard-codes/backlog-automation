import httpx

from backlog_automation.config import settings

BASE_URL = "https://api.figma.com/v1"
HEADERS = {"X-Figma-Token": settings.figma_access_token}


def publish_frames(frames: list[dict]) -> list[dict]:
    """Create a Figma file with annotated wireframe frames for each spec."""
    # Create a new Figma file in the team
    file_resp = httpx.post(
        f"{BASE_URL}/files",
        headers=HEADERS,
        json={"name": "Backlog Wireframes", "team_id": settings.figma_team_id},
    )
    file_resp.raise_for_status()
    file_key = file_resp.json()["key"]

    created = []
    for frame in frames:
        annotation_text = "\n".join(frame.get("annotations", []))
        components_text = ", ".join(frame.get("components", []))

        # Add a frame node with a sticky-note style text block
        node_resp = httpx.post(
            f"{BASE_URL}/files/{file_key}/nodes",
            headers=HEADERS,
            json={
                "nodes": [
                    {
                        "type": "FRAME",
                        "name": frame["name"],
                        "children": [
                            {
                                "type": "TEXT",
                                "name": "Spec",
                                "characters": (
                                    f"{frame['description']}\n\n"
                                    f"Components: {components_text}\n\n"
                                    f"Annotations:\n{annotation_text}"
                                ),
                            }
                        ],
                    }
                ]
            },
        )
        node_resp.raise_for_status()
        created.append({"frame": frame["name"], "file_key": file_key})

    return created
