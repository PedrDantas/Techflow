"""
Camada de armazenamento do TaskFlow.
Gerencia persistência de tarefas em arquivo JSON.
"""

import json
import os
from typing import List, Optional
from models import Task, TaskStatus, TaskPriority


DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
DATA_FILE = os.path.join(DATA_DIR, 'tasks.json')


class Storage:
    """
    Gerencia a persistência das tarefas em arquivo JSON.

    Métodos:
        save(task): Salva nova tarefa.
        get_all(): Retorna todas as tarefas.
        get_by_id(task_id): Retorna tarefa por ID.
        update(task): Atualiza tarefa existente.
        delete(task_id): Remove tarefa pelo ID.
        get_by_status(status): Filtra tarefas por status.
        get_by_priority(priority): Filtra tarefas por prioridade.
    """

    def __init__(self, filepath: str = DATA_FILE):
        self.filepath = filepath
        self._ensure_file()

    def _ensure_file(self):
        """Garante que o arquivo de dados existe."""
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        if not os.path.exists(self.filepath):
            self._write([])

    def _read(self) -> List[dict]:
        """Lê todos os dados do arquivo JSON."""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _write(self, data: List[dict]):
        """Escreve dados no arquivo JSON."""
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def save(self, task: Task):
        """Persiste uma nova tarefa."""
        data = self._read()
        data.append(task.to_dict())
        self._write(data)

    def get_all(self) -> List[Task]:
        """Retorna todas as tarefas armazenadas."""
        return [Task.from_dict(d) for d in self._read()]

    def get_by_id(self, task_id: str) -> Optional[Task]:
        """Busca uma tarefa pelo seu ID único."""
        for item in self._read():
            if item["id"] == task_id:
                return Task.from_dict(item)
        return None

    def update(self, task: Task):
        """Atualiza os dados de uma tarefa existente."""
        data = self._read()
        for i, item in enumerate(data):
            if item["id"] == task.id:
                data[i] = task.to_dict()
                self._write(data)
                return
        raise ValueError(f"Tarefa com ID '{task.id}' não encontrada.")

    def delete(self, task_id: str) -> bool:
        """Remove uma tarefa pelo ID. Retorna True se removida."""
        data = self._read()
        new_data = [item for item in data if item["id"] != task_id]
        if len(new_data) == len(data):
            return False
        self._write(new_data)
        return True

    def get_by_status(self, status: TaskStatus) -> List[Task]:
        """Filtra e retorna tarefas por status."""
        return [t for t in self.get_all() if t.status == status]

    def get_by_priority(self, priority: TaskPriority) -> List[Task]:
        """Filtra e retorna tarefas por prioridade."""
        return [t for t in self.get_all() if t.priority == priority]

    def count(self) -> int:
        """Retorna o total de tarefas armazenadas."""
        return len(self._read())
