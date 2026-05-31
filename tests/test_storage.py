"""
Testes unitários para o módulo storage.py
Valida as operações CRUD de persistência de tarefas.
Testes unitários para validação da camada de persistência JSON

"""

import pytest
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from models import Task, TaskStatus, TaskPriority
from storage import Storage


@pytest.fixture
def temp_storage():
    """Fixture que cria um Storage temporário para cada teste."""
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
        filepath = f.name
    storage = Storage(filepath=filepath)
    yield storage
    # Limpeza após o teste
    if os.path.exists(filepath):
        os.unlink(filepath)


class TestStorageSave:
    """Testes de criação (CREATE)."""

    def test_save_task(self, temp_storage):
        """Deve salvar uma tarefa com sucesso."""
        task = Task(title="Tarefa de teste")
        temp_storage.save(task)
        assert temp_storage.count() == 1

    def test_save_multiple_tasks(self, temp_storage):
        """Deve salvar múltiplas tarefas."""
        for i in range(3):
            temp_storage.save(Task(title=f"Tarefa {i}"))
        assert temp_storage.count() == 3


class TestStorageRead:
    """Testes de leitura (READ)."""

    def test_get_all_empty(self, temp_storage):
        """get_all() deve retornar lista vazia quando não há tarefas."""
        assert temp_storage.get_all() == []

    def test_get_all_returns_tasks(self, temp_storage):
        """get_all() deve retornar todas as tarefas salvas."""
        temp_storage.save(Task(title="T1"))
        temp_storage.save(Task(title="T2"))
        tasks = temp_storage.get_all()
        assert len(tasks) == 2

    def test_get_by_id_found(self, temp_storage):
        """get_by_id() deve retornar a tarefa correta."""
        task = Task(title="Buscar por ID")
        temp_storage.save(task)
        found = temp_storage.get_by_id(task.id)
        assert found is not None
        assert found.title == "Buscar por ID"

    def test_get_by_id_not_found(self, temp_storage):
        """get_by_id() deve retornar None para ID inexistente."""
        result = temp_storage.get_by_id("id-inexistente")
        assert result is None


class TestStorageUpdate:
    """Testes de atualização (UPDATE)."""

    def test_update_task_title(self, temp_storage):
        """Deve atualizar o título de uma tarefa."""
        task = Task(title="Título antigo")
        temp_storage.save(task)

        task.title = "Título novo"
        temp_storage.update(task)

        updated = temp_storage.get_by_id(task.id)
        assert updated.title == "Título novo"

    def test_update_task_status(self, temp_storage):
        """Deve atualizar o status de uma tarefa."""
        task = Task(title="Atualizar status")
        temp_storage.save(task)

        task.status = TaskStatus.DONE
        temp_storage.update(task)

        updated = temp_storage.get_by_id(task.id)
        assert updated.status == TaskStatus.DONE

    def test_update_nonexistent_task_raises(self, temp_storage):
        """Atualizar tarefa inexistente deve levantar ValueError."""
        task = Task(title="Não existe", task_id="fake-id")
        with pytest.raises(ValueError):
            temp_storage.update(task)


class TestStorageDelete:
    """Testes de exclusão (DELETE)."""

    def test_delete_task(self, temp_storage):
        """Deve excluir uma tarefa com sucesso."""
        task = Task(title="Para excluir")
        temp_storage.save(task)
        assert temp_storage.count() == 1

        result = temp_storage.delete(task.id)
        assert result is True
        assert temp_storage.count() == 0

    def test_delete_nonexistent_returns_false(self, temp_storage):
        """Excluir ID inexistente deve retornar False."""
        result = temp_storage.delete("id-que-nao-existe")
        assert result is False


class TestStorageFilters:
    """Testes de filtragem de tarefas."""

    def test_filter_by_status(self, temp_storage):
        """Deve filtrar tarefas pelo status correto."""
        temp_storage.save(Task(title="T1", status=TaskStatus.TODO))
        temp_storage.save(Task(title="T2", status=TaskStatus.DONE))
        temp_storage.save(Task(title="T3", status=TaskStatus.TODO))

        todo_tasks = temp_storage.get_by_status(TaskStatus.TODO)
        assert len(todo_tasks) == 2

    def test_filter_by_priority(self, temp_storage):
        """Deve filtrar tarefas pela prioridade correta."""
        temp_storage.save(Task(title="T1", priority=TaskPriority.HIGH))
        temp_storage.save(Task(title="T2", priority=TaskPriority.LOW))
        temp_storage.save(Task(title="T3", priority=TaskPriority.HIGH))

        high_tasks = temp_storage.get_by_priority(TaskPriority.HIGH)
        assert len(high_tasks) == 2
