"""
Testes unitários para o módulo models.py
Valida criação, serialização e comportamento da classe Task.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from models import Task, TaskStatus, TaskPriority


class TestTaskCreation:
    """Testes de criação de instâncias Task."""

    def test_create_task_with_required_fields(self):
        """Deve criar tarefa com título obrigatório."""
        task = Task(title="Implementar login")
        assert task.title == "Implementar login"
        assert task.id is not None

    def test_create_task_default_status_is_todo(self):
        """Tarefa criada deve ter status TODO por padrão."""
        task = Task(title="Nova tarefa")
        assert task.status == TaskStatus.TODO

    def test_create_task_default_priority_is_medium(self):
        """Tarefa criada deve ter prioridade MEDIUM por padrão."""
        task = Task(title="Nova tarefa")
        assert task.priority == TaskPriority.MEDIUM

    def test_create_task_with_all_fields(self):
        """Deve criar tarefa com todos os campos preenchidos."""
        task = Task(
            title="Criar API",
            description="Criar endpoints REST",
            status=TaskStatus.IN_PROGRESS,
            priority=TaskPriority.HIGH,
            assignee="João Silva"
        )
        assert task.title == "Criar API"
        assert task.description == "Criar endpoints REST"
        assert task.status == TaskStatus.IN_PROGRESS
        assert task.priority == TaskPriority.HIGH
        assert task.assignee == "João Silva"

    def test_task_id_is_unique(self):
        """IDs de tarefas diferentes devem ser únicos."""
        task1 = Task(title="Tarefa 1")
        task2 = Task(title="Tarefa 2")
        assert task1.id != task2.id

    def test_task_has_created_at(self):
        """Tarefa deve ter data de criação definida."""
        task = Task(title="Tarefa com data")
        assert task.created_at is not None
        assert len(task.created_at) > 0


class TestTaskSerialization:
    """Testes de serialização e desserialização de Task."""

    def test_to_dict_returns_dict(self):
        """to_dict() deve retornar um dicionário."""
        task = Task(title="Tarefa teste")
        result = task.to_dict()
        assert isinstance(result, dict)

    def test_to_dict_contains_required_keys(self):
        """Dicionário deve conter todas as chaves esperadas."""
        task = Task(title="Tarefa teste")
        result = task.to_dict()
        expected_keys = {"id", "title", "description", "status", "priority", "assignee", "created_at", "updated_at"}
        assert expected_keys.issubset(result.keys())

    def test_to_dict_status_is_string(self):
        """Status no dicionário deve ser string, não Enum."""
        task = Task(title="Tarefa", status=TaskStatus.DONE)
        result = task.to_dict()
        assert result["status"] == "done"
        assert isinstance(result["status"], str)

    def test_from_dict_recreates_task(self):
        """from_dict() deve recriar a tarefa com os mesmos dados."""
        original = Task(
            title="Tarefa original",
            description="Descrição",
            status=TaskStatus.IN_PROGRESS,
            priority=TaskPriority.HIGH,
            assignee="Maria"
        )
        data = original.to_dict()
        restored = Task.from_dict(data)

        assert restored.id == original.id
        assert restored.title == original.title
        assert restored.status == original.status
        assert restored.priority == original.priority
        assert restored.assignee == original.assignee

    def test_roundtrip_serialization(self):
        """Tarefa deve sobreviver a ciclo completo de serialização."""
        task = Task(title="Roundtrip test", assignee="Dev")
        restored = Task.from_dict(task.to_dict())
        assert task.id == restored.id
        assert task.title == restored.title


class TestTaskStatus:
    """Testes para os valores de TaskStatus."""

    def test_status_values(self):
        """Deve ter os três status esperados."""
        assert TaskStatus.TODO.value == "todo"
        assert TaskStatus.IN_PROGRESS.value == "in_progress"
        assert TaskStatus.DONE.value == "done"

    def test_status_from_string(self):
        """Deve criar status a partir de string."""
        assert TaskStatus("todo") == TaskStatus.TODO
        assert TaskStatus("in_progress") == TaskStatus.IN_PROGRESS
        assert TaskStatus("done") == TaskStatus.DONE


class TestTaskPriority:
    """Testes para os valores de TaskPriority."""

    def test_priority_values(self):
        """Deve ter os três níveis de prioridade esperados."""
        assert TaskPriority.LOW.value == "low"
        assert TaskPriority.MEDIUM.value == "medium"
        assert TaskPriority.HIGH.value == "high"
