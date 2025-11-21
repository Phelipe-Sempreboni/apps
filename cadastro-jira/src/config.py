from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()

@dataclass
class JiraConfig:
    base_url: str
    email: str
    api_token: str
    project_key: str
    issue_type: str = "Story"

    @classmethod
    def from_env(cls) -> "JiraConfig":
        return cls(
            base_url=os.environ["JIRA_BASE_URL"].rstrip("/"),
            email=os.environ["JIRA_EMAIL"],
            api_token=os.environ["JIRA_API_TOKEN"],
            project_key=os.environ["JIRA_PROJECT_KEY"],
            issue_type=os.environ.get("JIRA_ISSUE_TYPE", "Story"),
        )
