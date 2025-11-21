# src/logging_db.py

import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional


# Caminho do DB: <raiz do projeto>/data/app_logs.db
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "data" / "app_logs.db"


@dataclass
class IssueLogEntry:
    source: str           # ex.: "cli_single", "cli_bulk", "ui_yaml", "ui_single"
    issue_key: str        # ex.: "DOCKER-123"
    title: str
    description: str
    n_tasks: int
    project_key: str
    issue_type: str       # ex.: "Task", "Story"


@dataclass
class AppLogEntry:
    level: str            # "INFO", "WARN", "ERROR"
    context: str          # ex.: "ui_yaml_create", "cli_bulk"
    message: str
    details: Optional[str] = None


def _get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn


def init_db() -> None:
    """
    Cria as tabelas de logs, se ainda não existirem.
    Pode ser chamado várias vezes (idempotente).
    """
    conn = _get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS issue_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            source TEXT NOT NULL,
            issue_key TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            n_tasks INTEGER NOT NULL,
            project_key TEXT NOT NULL,
            issue_type TEXT NOT NULL
        );
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS app_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            level TEXT NOT NULL,
            context TEXT NOT NULL,
            message TEXT NOT NULL,
            details TEXT
        );
        """
    )

    conn.commit()
    conn.close()


def log_issue_creation(entry: IssueLogEntry) -> None:
    """
    Registra no SQLite uma história criada no Jira.
    """
    conn = _get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO issue_history (
            created_at, source, issue_key, title, description,
            n_tasks, project_key, issue_type
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """,
        (
            datetime.utcnow().isoformat(timespec="seconds") + "Z",
            entry.source,
            entry.issue_key,
            entry.title,
            entry.description,
            entry.n_tasks,
            entry.project_key,
            entry.issue_type,
        ),
    )

    conn.commit()
    conn.close()


def log_app_event(entry: AppLogEntry) -> None:
    """
    Registra um evento operacional/de negócio no SQLite.
    """
    conn = _get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO app_log (
            created_at, level, context, message, details
        )
        VALUES (?, ?, ?, ?, ?);
        """,
        (
            datetime.utcnow().isoformat(timespec="seconds") + "Z",
            entry.level,
            entry.context,
            entry.message,
            entry.details,
        ),
    )

    conn.commit()
    conn.close()
