from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Story:
    title: str
    description: str
    tasks: List[str] = field(default_factory=list)

    def full_description(self) -> str:
        if not self.tasks:
            return self.description

        bullets = "\n".join(f"- {t}" for t in self.tasks)
        return f"{self.description}\n\nTarefas:\n{bullets}"
