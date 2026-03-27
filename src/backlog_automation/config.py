from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Anthropic
    anthropic_api_key: str

    # Atlassian
    atlassian_url: str
    atlassian_username: str
    atlassian_api_token: str
    jira_project_key: str
    confluence_space_key: str

    # Figma
    figma_access_token: str
    figma_team_id: str


settings = Settings()
