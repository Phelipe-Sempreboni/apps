# src/main.py

import argparse
from typing import List

from .config import JiraConfig
from .jira_client import JiraClient
from .models import Story
from .loaders.yaml_loader import load_stories_from_yaml
from .use_cases.create_single_issue import create_single_story
from .use_cases.create_bulk_issues import create_bulk_stories
from .logging_db import init_db, IssueLogEntry, log_issue_creation


def _create_example_story() -> Story:
    return Story(
        title="[Teste] - História criada via API (single)",
        description="História de teste criada via script Python usando Jira REST API.",
        tasks=[
            "Validar se a história foi criada no Jira.",
            "Verificar se o título e a descrição estão corretos.",
        ],
    )


def _create_two_example_stories() -> List[Story]:
    return [
        Story(
            title="[Teste] - História 1 criada via API (duas histórias)",
            description="Primeira história de teste criada quando o modo 'test-two' é usado.",
        ),
        Story(
            title="[Teste] - História 2 criada via API (duas histórias)",
            description="Segunda história de teste criada quando o modo 'test-two' é usado.",
        ),
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Cadastro automático de histórias no Jira.")
    parser.add_argument(
        "--mode",
        choices=["single", "test-two", "bulk"],
        default="single",
        help="single = 1 história de teste; test-two = 2 histórias; bulk = ler de arquivo YAML.",
    )
    parser.add_argument(
        "--input-file",
        "-i",
        default="data/stories_example.yaml",
        help="Caminho para o YAML com histórias (modo bulk).",
    )

    args = parser.parse_args()

    config = JiraConfig.from_env()
    jira_client = JiraClient(config)

    # Inicializa o banco de logs (idempotente)
    init_db()

    if args.mode == "single":
        story = _create_example_story()
        description = story.full_description()
        issue_key = jira_client.create_issue(summary=story.title, description=description)

        log_issue_creation(
            IssueLogEntry(
                source="cli_single",
                issue_key=issue_key,
                title=story.title,
                description=story.description,
                n_tasks=len(story.tasks),
                project_key=config.project_key,
                issue_type=config.issue_type,
            )
        )

        print(f"História criada com sucesso: {issue_key}")

    elif args.mode == "test-two":
        stories = _create_two_example_stories()
        keys = create_bulk_stories(jira_client, stories)

        for story, key in zip(stories, keys):
            log_issue_creation(
                IssueLogEntry(
                    source="cli_test_two",
                    issue_key=key,
                    title=story.title,
                    description=story.description,
                    n_tasks=len(story.tasks),
                    project_key=config.project_key,
                    issue_type=config.issue_type,
                )
            )

        print(f"Histórias criadas com sucesso: {', '.join(keys)}")

    elif args.mode == "bulk":
        stories = load_stories_from_yaml(args.input_file)
        keys = create_bulk_stories(jira_client, stories)

        for story, key in zip(stories, keys):
            log_issue_creation(
                IssueLogEntry(
                    source="cli_bulk",
                    issue_key=key,
                    title=story.title,
                    description=story.description,
                    n_tasks=len(story.tasks),
                    project_key=config.project_key,
                    issue_type=config.issue_type,
                )
            )

        print(f"{len(keys)} histórias criadas com sucesso: {', '.join(keys)}")


if __name__ == "__main__":
    main()
