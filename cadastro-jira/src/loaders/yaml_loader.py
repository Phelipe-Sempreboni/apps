# src/loaders/yaml_loader.py

from typing import List, Any
import pathlib

import yaml

from ..models import Story


def _normalize_tasks(raw_tasks: Any) -> List[str]:
    """
    Normaliza o campo 'tasks' vindo do YAML.

    Regras:
    - Se for string: separa por ';'
    - Se for lista:
        - Cada item string pode ter vários tasks separados por ';'
    - Se não vier nada: lista vazia
    """
    tasks: List[str] = []

    if isinstance(raw_tasks, str):
        parts = [p.strip() for p in raw_tasks.split(";") if p.strip()]
        tasks.extend(parts)

    elif isinstance(raw_tasks, list):
        for item in raw_tasks:
            if isinstance(item, str):
                parts = [p.strip() for p in item.split(";") if p.strip()]
                tasks.extend(parts)

    # Se não for string nem lista, ignora
    return tasks


def stories_from_raw_list(raw: List[dict]) -> List[Story]:
    """
    Converte uma lista crua (vinda de yaml.safe_load) em uma lista de Story.
    """
    stories: List[Story] = []

    for item in raw:
        title = item.get("title", "").strip()
        if not title:
            # ignora itens sem título
            continue

        description = item.get("description", "").strip()
        raw_tasks = item.get("tasks", [])
        tasks = _normalize_tasks(raw_tasks)

        stories.append(
            Story(
                title=title,
                description=description,
                tasks=tasks,
            )
        )

    return stories


def parse_stories_from_yaml_text(yaml_text: str) -> List[Story]:
    """
    Converte o texto de configuração em histórias.

    Suporta três formas:

    1) YAML com lista de histórias:
       - title: ...
       - title: ...

    2) YAML de uma única história (dict):
       title: ...
       description: ...

    3) Multiblocos separados por linhas contendo apenas ';':
       [bloco YAML 1]
       ;
       [bloco YAML 2]
       ;
       [bloco YAML 3]
    """
    text = yaml_text.strip()
    if not text:
        return []

    lines = text.splitlines()
    has_semicolon_separator = any(line.strip() == ";" for line in lines)

    blocks: List[str] = []

    if has_semicolon_separator:
        buffer: List[str] = []
        for line in lines:
            if line.strip() == ";":
                block = "\n".join(buffer).strip()
                if block:
                    blocks.append(block)
                buffer = []
            else:
                buffer.append(line)
        # último bloco (se não terminar com ;)
        block = "\n".join(buffer).strip()
        if block:
            blocks.append(block)
    else:
        # Sem ';' → trata tudo como um único bloco
        blocks = [text]

    all_stories: List[Story] = []

    for block in blocks:
        if not block.strip():
            continue

        raw = yaml.safe_load(block) or []

        # Pode ser:
        # - dict (uma história)
        # - list (várias histórias)
        if isinstance(raw, dict):
            raw_list = [raw]
        elif isinstance(raw, list):
            raw_list = raw
        else:
            raise ValueError(
                "Cada bloco YAML deve ser um objeto (dict) ou uma lista de objetos.\n"
                "Bloco problemático:\n"
                f"{block}"
            )

        stories = stories_from_raw_list(raw_list)
        all_stories.extend(stories)

    return all_stories


def load_stories_from_yaml(path: str) -> List[Story]:
    """
    Lê o arquivo no caminho informado e usa o mesmo parser de texto.
    """
    file_path = pathlib.Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"Arquivo YAML não encontrado: {file_path}")

    text = file_path.read_text(encoding="utf-8")
    return parse_stories_from_yaml_text(text)
