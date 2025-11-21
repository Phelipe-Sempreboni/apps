import base64
import json
from typing import Dict, Any, List

import requests

from .config import JiraConfig


class JiraClient:
    def __init__(self, config: JiraConfig):
        self._config = config
        token_bytes = f"{config.email}:{config.api_token}".encode("utf-8")
        basic_token = base64.b64encode(token_bytes).decode("utf-8")

        self._headers = {
            "Authorization": f"Basic {basic_token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def _build_adf_description(self, description_text: str) -> Dict[str, Any]:
        """
        Converte uma string simples para um documento no formato Atlassian (ADF).
        Cada parágrafo (separado por linha em branco) vira um 'paragraph'.
        """
        # Quebra o texto em parágrafos usando linha em branco como separador
        raw_paragraphs: List[str] = description_text.split("\n\n")
        content: List[Dict[str, Any]] = []

        for paragraph in raw_paragraphs:
            # Se quiser ignorar linhas totalmente vazias:
            if not paragraph.strip():
                continue

            content.append(
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": paragraph,
                        }
                    ],
                }
            )

        # Se por algum motivo tudo estiver vazio, garante ao menos um parágrafo
        if not content:
            content.append(
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": "",
                        }
                    ],
                }
            )

        return {
            "type": "doc",
            "version": 1,
            "content": content,
        }

    def create_issue(self, summary: str, description: str) -> str:
        """
        Cria uma issue no Jira e retorna a chave (ex.: DOCKER-123).
        Em caso de erro, imprime a resposta detalhada do Jira.
        """
        url = f"{self._config.base_url}/rest/api/3/issue"

        description_doc = self._build_adf_description(description)

        payload: Dict[str, Any] = {
            "fields": {
                "project": {"key": self._config.project_key},
                "summary": summary,
                "description": description_doc,
                "issuetype": {"name": self._config.issue_type},
            }
        }

        response = requests.post(url, json=payload, headers=self._headers, timeout=30)

        if response.status_code >= 400:
            print("\n[ERRO JIRA] Status:", response.status_code)
            try:
                data = response.json()
                print("[ERRO JIRA] Corpo JSON:")
                print(json.dumps(data, indent=2, ensure_ascii=False))
            except ValueError:
                print("[ERRO JIRA] Corpo texto:")
                print(response.text)

            response.raise_for_status()

        data = response.json()
        return data["key"]
