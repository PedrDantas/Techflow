"""
Modelos de dados do sistema TaskFlow.
Define as estruturas Task, TaskStatus e TaskPriority.
Modelos de dados do TaskFlow: Task, TaskStatus e TaskPriority
"""

from enum import Enum
from datetime import datetime
import uuid


class TaskStatus(Enum):
    """Status possíveis de uma tarefa no fluxo Kanban."""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskPriority(Enum):
    """Níveis de prioridade de uma tarefa."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Task:
    """
    Representa uma tarefa no sistema de gerenciamento.

    Atributos:
        id (str): Identificador único da tarefa (UUID).
        title (str): Título da tarefa.
        description (str): Descrição detalhada.
        status (TaskStatus): Status atual da tarefa.
        priority (TaskPriority): Nível de prioridade.
        assignee (str): Nome do responsável pela tarefa.
        created_at (str): Data/hora de criação (ISO format).
        updated_at (str): Data/hora da última atualização (ISO format).
    """

    def __init__(
        self,
        title: str,
        description: str = "",
        status: TaskStatus = TaskStatus.TODO,
        priority: TaskPriority = TaskPriority.MEDIUM,
        assignee: str = "",
        task_id: str = None,
        created_at: str = None,
        updated_at: str = None
    ):
        self.id = task_id or str(uuid.uuid4())[:8]
        self.title = title
        self.description = description
        self.status = status
        self.priority = priority
        self.assignee = assignee
        self.created_at = created_at or datetime.utcnow().isoformat()
        self.updated_at = updated_at or datetime.utcnow().isoformat()

    def to_dict(self) -> dict:
        """Converte a tarefa para dicionário (para serialização JSON)."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "priority": self.priority.value,
            "assignee": self.assignee,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Cria uma instância de Task a partir de um dicionário."""
        return cls(
            title=data["title"],
            description=data.get("description", ""),
            status=TaskStatus(data.get("status", "todo")),
            priority=TaskPriority(data.get("priority", "medium")),
            assignee=data.get("assignee", ""),
            task_id=data.get("id"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )

    def __repr__(self):
        return f"Task(id={self.id}, title='{self.title}', status={self.status.value})"
