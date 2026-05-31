"""
Testes unitários para o módulo notifier.py
Valida a lógica de notificação sem enviar e-mails reais.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from models import Task, TaskStatus, TaskPriority
from notifier import Notifier


@pytest.fixture
def notifier():
    """Fixture que cria um Notifier desabilitado para testes."""
    return Notifier(enabled=False)


@pytest.fixture
def active_notifier():
    """Fixture que cria um Notifier habilitado para testes de lógica."""
    return Notifier(enabled=True)


class TestNotifierShouldNotify:
    """Testes para a lógica de decisão de notificação."""

    def test_should_notify_high_priority_with_assignee(self, active_notifier):
        """Deve notificar tarefas de alta prioridade com responsável."""
        task = Task(title="Urgente", priority=TaskPriority.HIGH, assignee="João")
        assert active_notifier.should_notify(task) is True

    def test_should_not_notify_low_priority(self, active_notifier):
        """Não deve notificar tarefas de baixa prioridade."""
        task = Task(title="Menor urgência", priority=TaskPriority.LOW, assignee="João")
        assert active_notifier.should_notify(task) is False

    def test_should_not_notify_without_assignee(self, active_notifier):
        """Não deve notificar tarefas sem responsável definido."""
        task = Task(title="Sem responsável", priority=TaskPriority.HIGH, assignee="")
        assert active_notifier.should_notify(task) is False

    def test_should_not_notify_when_disabled(self, notifier):
        """Não deve notificar quando o notifier está desabilitado."""
        task = Task(title="Alta prioridade", priority=TaskPriority.HIGH, assignee="Maria")
        assert notifier.should_notify(task) is False

    def test_should_not_notify_medium_priority(self, active_notifier):
        """Não deve notificar tarefas de prioridade média."""
        task = Task(title="Média prioridade", priority=TaskPriority.MEDIUM, assignee="Carlos")
        assert active_notifier.should_notify(task) is False


class TestNotifierBuildMessage:
    """Testes para a construção da mensagem de notificação."""

    def test_message_contains_task_title(self, active_notifier):
        """Mensagem deve conter o título da tarefa."""
        task = Task(title="Implementar autenticação", assignee="Ana")
        message = active_notifier.build_message(task)
        assert "Implementar autenticação" in message

    def test_message_contains_assignee_name(self, active_notifier):
        """Mensagem deve conter o nome do responsável."""
        task = Task(title="Tarefa X", assignee="Pedro")
        message = active_notifier.build_message(task)
        assert "Pedro" in message

    def test_message_contains_event_type(self, active_notifier):
        """Mensagem deve indicar o tipo de evento."""
        task = Task(title="Tarefa Y", assignee="Lucia")
        message_created = active_notifier.build_message(task, event="criada")
        message_updated = active_notifier.build_message(task, event="atualizada")
        assert "criada" in message_created
        assert "atualizada" in message_updated

    def test_send_returns_false_when_disabled(self, notifier):
        """send() deve retornar False quando desabilitado."""
        task = Task(title="Teste", priority=TaskPriority.HIGH, assignee="Dev")
        result = notifier.send("dev@email.com", task)
        assert result is False
