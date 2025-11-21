from ..jira_client import JiraClient
from ..models import Story

def create_single_story(jira_client: JiraClient, story: Story) -> str:
    """
    Orquestra a criação de uma única história no Jira.
    """
    description = story.full_description()
    issue_key = jira_client.create_issue(summary=story.title, description=description)
    return issue_key
