from typing import Iterable, List

from ..jira_client import JiraClient
from ..models import Story
from .create_single_issue import create_single_story


def create_bulk_stories(jira_client: JiraClient, stories: Iterable[Story]) -> List[str]:
    """
    Cria várias histórias em sequência e retorna a lista de chaves.
    """
    keys: List[str] = []

    for story in stories:
        issue_key = create_single_story(jira_client, story)
        keys.append(issue_key)

    return keys
