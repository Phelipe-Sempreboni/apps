# src/ui/streamlit_app.py

import traceback
from typing import List

import pandas as pd
import streamlit as st

import sys
from pathlib import Path

# Adiciona o diretório raiz do projeto ao sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import JiraConfig
from src.jira_client import JiraClient
from src.models import Story
from src.loaders.yaml_loader import parse_stories_from_yaml_text
from src.use_cases.create_single_issue import create_single_story
from src.use_cases.create_bulk_issues import create_bulk_stories
from src.logging_db import init_db, IssueLogEntry, log_issue_creation, AppLogEntry, log_app_event


YAML_FILE_PATH = PROJECT_ROOT / "data" / "stories_example.yaml"


@st.cache_resource
def get_jira_client() -> JiraClient:
    """
    Cria e reaproveita uma instância de JiraClient.
    """
    config = JiraConfig.from_env()
    return JiraClient(config)


def _build_issue_url(config: JiraConfig, issue_key: str) -> str:
    """
    Monta a URL da issue no Jira.
    """
    return f"{config.base_url}/browse/{issue_key}"


def _parse_tasks_input(tasks_text: str) -> List[str]:
    """
    Converte o texto digitado no campo de tarefas em uma lista de strings.
    Cada linha vira uma tarefa.
    """
    return [line.strip() for line in tasks_text.splitlines() if line.strip()]


def load_yaml_text_from_file() -> str:
    """
    Carrega o conteúdo do stories_example.yaml (se existir),
    ou retorna um exemplo padrão (com blocos separados por ';').
    """
    if YAML_FILE_PATH.exists():
        return YAML_FILE_PATH.read_text(encoding="utf-8")

    # Exemplo padrão com dois blocos separados por ';'
    return """- title: "[Usuário Sirius] - Criar usuário dedicado no notebook para o curso de Docker"
  description: >
    Criar um novo usuário no notebook exclusivo para a Sirius, usado nos cursos de Docker,
    separando o ambiente de estudos do ambiente pessoal.
  tasks:
    - Criar usuário dedicado no sistema operacional.
    - Configurar permissões mínimas (docker, git, editor).
    - Organizar diretórios padrão de projetos da Sirius.
    - Documentar o passo a passo para os alunos.

;
- title: "[Jornada Docker] - Estruturar curso com Dockerfiles e Composes manuais antes de automações"
  description: >
    Definir e documentar a jornada didática em que os alunos criam Dockerfiles e docker-compose
    manualmente, para só depois evoluir para scripts automatizados.
  tasks:
    - Mapear módulos onde Dockerfiles e Compose serão criados manualmente.
    - Definir sequência didática com comandos docker puros, Dockerfile, Compose e automação.
    - Criar exemplos práticos focados no uso de CLI.
"""


def save_yaml_text_to_file(text: str) -> None:
    """
    Salva o texto YAML no arquivo stories_example.yaml.
    """
    YAML_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
    YAML_FILE_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    st.set_page_config(
        page_title="Cadastro de Histórias no Jira",
        page_icon="✅",
        layout="wide",
    )

    st.title("Cadastro de Histórias no Jira via YAML")
    st.caption("Edite a configuração (como o stories_example.yaml) e envie tudo para o Jira em lote.")

    config = JiraConfig.from_env()
    jira_client = get_jira_client()

    # Inicializa o banco de logs (idempotente)
    init_db()

    with st.sidebar:
        st.subheader("Configuração (somente leitura)")
        st.text_input("Jira Base URL", value=config.base_url, disabled=True)
        st.text_input("Projeto (KEY)", value=config.project_key, disabled=True)
        st.text_input("Issue Type", value=config.issue_type, disabled=True)
        st.markdown("---")
        st.markdown(
            "As credenciais (email + token) são carregadas do `.env`.\n\n"
            "Este app lê/grava o arquivo `data/stories_example.yaml`."
        )

    tab_yaml, tab_single = st.tabs(["🧾 Modo YAML (recomendado)", "➕ Modo simples (1 história)"])

    # --- Aba 1: Modo YAML ---
    with tab_yaml:
        st.subheader("Editar YAML de histórias (stories_example.yaml)")

        st.markdown(
            """
            **Como usar este modo:**
            
            - Você pode escrever **uma única história** em YAML (sem `;`), ou  
            - Várias histórias, separando blocos com uma linha que contenha apenas `;`, por exemplo:
            
            ```yaml
            - title: "[Usuário Sirius] - Criar usuário dedicado..."
              description: >
                Criar um novo usuário no notebook exclusivo para a Sirius.
              tasks:
                - Criar usuário dedicado...
                - Configurar permissões mínimas...

            ;
            - title: "[Jornada Docker] - Estruturar curso com Dockerfiles e Composes"
              description: >
                Definir e documentar a jornada didática...
              tasks:
                - Mapear módulos...
                - Definir sequência didática...
                - Criar exemplos práticos...
            ```
            
            - O arquivo editado aqui é o `data/stories_example.yaml`.  
            - O botão **Pré-visualizar histórias** mostra como o app interpretou esse conteúdo.  
            """
        )

        # Carrega texto inicial só uma vez na sessão
        if "yaml_text" not in st.session_state:
            st.session_state.yaml_text = load_yaml_text_from_file()

        yaml_text = st.text_area(
            "Config YAML das histórias",
            height=400,
            key="yaml_text",
        )

        col1, col2, col3 = st.columns(3)

        if col1.button("💾 Salvar YAML no arquivo"):
            try:
                save_yaml_text_to_file(yaml_text)
            except Exception as e:
                st.error("Erro ao salvar o YAML no arquivo.")
                st.code("".join(traceback.format_exception(e)), language="text")
                log_app_event(
                    AppLogEntry(
                        level="ERROR",
                        context="ui_yaml_save",
                        message="Erro ao salvar YAML",
                        details="".join(traceback.format_exception(e)),
                    )
                )
            else:
                st.success(f"YAML salvo em: {YAML_FILE_PATH}")

        preview_clicked = col2.button("👀 Pré-visualizar histórias")
        create_clicked = col3.button("🚀 Criar histórias no Jira")

        if preview_clicked or create_clicked:
            try:
                stories = parse_stories_from_yaml_text(yaml_text)
            except Exception as e:
                st.error("Erro ao interpretar o YAML.")
                st.code(str(e), language="text")
                log_app_event(
                    AppLogEntry(
                        level="ERROR",
                        context="ui_yaml_parse",
                        message="Erro ao interpretar YAML",
                        details=str(e),
                    )
                )
            else:
                if not stories:
                    st.warning("Nenhuma história encontrada no YAML (verifique se há títulos preenchidos).")
                else:
                    # Pré-visualização
                    data = []
                    for s in stories:
                        data.append(
                            {
                                "title": s.title,
                                "description": (s.description[:120] + "...") if len(s.description) > 120 else s.description,
                                "n_tasks": len(s.tasks),
                                "tasks_preview": "; ".join(s.tasks[:5]),
                            }
                        )
                    df = pd.DataFrame(data)
                    st.dataframe(df, use_container_width=True)

                    if create_clicked:
                        with st.spinner(f"Criando {len(stories)} histórias no Jira..."):
                            try:
                                keys = create_bulk_stories(jira_client, stories)
                            except Exception as e:
                                st.error("Erro ao criar histórias no Jira.")
                                st.code("".join(traceback.format_exception(e)), language="text")
                                log_app_event(
                                    AppLogEntry(
                                        level="ERROR",
                                        context="ui_yaml_create",
                                        message="Erro ao criar histórias no Jira",
                                        details="".join(traceback.format_exception(e)),
                                    )
                                )
                            else:
                                st.success(f"{len(keys)} histórias criadas com sucesso.")
                                for story, key in zip(stories, keys):
                                    log_issue_creation(
                                        IssueLogEntry(
                                            source="ui_yaml",
                                            issue_key=key,
                                            title=story.title,
                                            description=story.description,
                                            n_tasks=len(story.tasks),
                                            project_key=config.project_key,
                                            issue_type=config.issue_type,
                                        )
                                    )
                                    url = _build_issue_url(config, key)
                                    st.markdown(f"- {key} → [Abrir no Jira]({url})")

    # --- Aba 2: Modo simples (1 história) ---
    with tab_single:
        st.subheader("Criar uma única história (modo rápido)")

        with st.form("single_story_form"):
            title = st.text_input(
                "Título da história",
                placeholder="[Tópico] - Descrição resumida da história",
            )
            description = st.text_area(
                "Descrição",
                placeholder="Descreva aqui o que precisa ser feito...",
                height=200,
            )
            tasks_text = st.text_area(
                "Tarefas (uma por linha, opcional)",
                placeholder="Tarefa 1\nTarefa 2\nTarefa 3",
                height=150,
            )

            submitted = st.form_submit_button("Criar história")

        if submitted:
            if not title.strip():
                st.error("O título é obrigatório.")
            else:
                tasks = _parse_tasks_input(tasks_text)
                story = Story(title=title.strip(), description=description.strip(), tasks=tasks)

                with st.spinner("Criando história no Jira..."):
                    try:
                        issue_key = create_single_story(jira_client, story)
                    except Exception as e:
                        st.error("Erro ao criar história no Jira.")
                        st.code("".join(traceback.format_exception(e)), language="text")
                        log_app_event(
                            AppLogEntry(
                                level="ERROR",
                                context="ui_single_create",
                                message="Erro ao criar história no Jira (modo single)",
                                details="".join(traceback.format_exception(e)),
                            )
                        )
                    else:
                        log_issue_creation(
                            IssueLogEntry(
                                source="ui_single",
                                issue_key=issue_key,
                                title=story.title,
                                description=story.description,
                                n_tasks=len(story.tasks),
                                project_key=config.project_key,
                                issue_type=config.issue_type,
                            )
                        )
                        issue_url = _build_issue_url(config, issue_key)
                        st.success(f"História criada com sucesso: {issue_key}")
                        st.markdown(f"[Abrir no Jira]({issue_url})")


if __name__ == "__main__":
    main()
