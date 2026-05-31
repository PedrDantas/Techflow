"""
Módulo de Notificações - TaskFlow
MUDANÇA DE ESCOPO: Adicionado na Sprint 3 a pedido do cliente.

Responsável por enviar alertas por e-mail quando tarefas
de alta prioridade são criadas ou atualizadas.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from models import Task, TaskPriority


class Notifier:
    """
    Gerencia o envio de notificações por e-mail para responsáveis
    de tarefas de alta prioridade.

    Atributos:
        smtp_host (str): Servidor SMTP.
        smtp_port (int): Porta do servidor SMTP.
        sender_email (str): E-mail remetente.
        sender_password (str): Senha do remetente.
        enabled (bool): Habilita/desabilita notificações.
    """

    def __init__(
        self,
        smtp_host: str = "smtp.gmail.com",
        smtp_port: int = 587,
        sender_email: str = "",
        sender_password: str = "",
        enabled: bool = True
    ):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.enabled = enabled

    def should_notify(self, task: Task) -> bool:
        """
        Verifica se uma tarefa deve gerar notificação.
        Notifica apenas tarefas de ALTA prioridade com responsável definido.
        """
        return (
            self.enabled
            and task.priority == TaskPriority.HIGH
            and bool(task.assignee)
        )

    def build_message(self, task: Task, event: str = "criada") -> str:
        """
        Monta o corpo da mensagem de notificação.

        Args:
            task: A tarefa que gerou o evento.
            event: Tipo de evento ('criada' ou 'atualizada').
        """
        return (
            f"Olá {task.assignee},\n\n"
            f"A tarefa de ALTA PRIORIDADE abaixo foi {event}:\n\n"
            f"  Título: {task.title}\n"
            f"  Descrição: {task.description or 'Sem descrição'}\n"
            f"  Status: {task.status.value}\n"
            f"  Criado em: {task.created_at[:10]}\n\n"
            f"Acesse o sistema TaskFlow para mais detalhes.\n\n"
            f"Equipe TechFlow Solutions"
        )

    def send(self, to_email: str, task: Task, event: str = "criada") -> bool:
        """
        Envia e-mail de notificação para o responsável.

        Args:
            to_email: E-mail do destinatário.
            task: Tarefa que gerou o evento.
            event: Tipo de evento.

        Returns:
            True se enviado com sucesso, False caso contrário.
        """
        if not self.enabled:
            return False

        try:
            msg = MIMEMultipart()
            msg["From"] = self.sender_email
            msg["To"] = to_email
            msg["Subject"] = f"[TaskFlow] ⚠️ Tarefa de Alta Prioridade {event}: {task.title}"

            body = self.build_message(task, event)
            msg.attach(MIMEText(body, "plain"))

            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, to_email, msg.as_string())

            return True

        except Exception:
            return False
