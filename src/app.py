"""
TaskFlow - Sistema de Gerenciamento de Tarefas
TechFlow Solutions | Projeto Ágil
Interface CLI principal do TaskFlow - CRUD de tarefas

"""

import json
import os
from datetime import datetime
from models import Task, TaskStatus, TaskPriority
from storage import Storage


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header():
    print("=" * 60)
    print("       TASKFLOW - Gerenciamento de Tarefas Ágeis")
    print("=" * 60)


def print_menu():
    print("\n📋 MENU PRINCIPAL")
    print("-" * 40)
    print("1. Criar nova tarefa")
    print("2. Listar todas as tarefas")
    print("3. Atualizar tarefa")
    print("4. Excluir tarefa")
    print("5. Filtrar por status")
    print("6. Filtrar por prioridade")
    print("0. Sair")
    print("-" * 40)


def create_task(storage: Storage):
    """Cria uma nova tarefa (CREATE)."""
    print("\n➕ CRIAR NOVA TAREFA")
    print("-" * 40)

    title = input("Título da tarefa: ").strip()
    if not title:
        print("❌ Título não pode estar vazio.")
        return

    description = input("Descrição: ").strip()

    print("Prioridade: 1-Baixa | 2-Média | 3-Alta")
    priority_input = input("Escolha (1-3): ").strip()
    priority_map = {"1": TaskPriority.LOW, "2": TaskPriority.MEDIUM, "3": TaskPriority.HIGH}
    priority = priority_map.get(priority_input, TaskPriority.MEDIUM)

    assignee = input("Responsável: ").strip()

    task = Task(
        title=title,
        description=description,
        priority=priority,
        assignee=assignee
    )

    storage.save(task)
    print(f"\n✅ Tarefa '{task.title}' criada com ID: {task.id}")


def list_tasks(storage: Storage, tasks=None):
    """Lista todas as tarefas (READ)."""
    if tasks is None:
        tasks = storage.get_all()

    print("\n📋 LISTA DE TAREFAS")
    print("-" * 60)

    if not tasks:
        print("Nenhuma tarefa encontrada.")
        return

    for task in tasks:
        status_icon = {"todo": "⬜", "in_progress": "🔄", "done": "✅"}.get(task.status.value, "⬜")
        priority_icon = {"low": "🟢", "medium": "🟡", "high": "🔴"}.get(task.priority.value, "🟡")

        print(f"\n{status_icon} [{task.id}] {task.title}")
        print(f"   {priority_icon} Prioridade: {task.priority.value.upper()}")
        print(f"   📝 {task.description or 'Sem descrição'}")
        print(f"   👤 Responsável: {task.assignee or 'Não atribuído'}")
        print(f"   📅 Criado em: {task.created_at[:10]}")

    print("-" * 60)
    print(f"Total: {len(tasks)} tarefa(s)")


def update_task(storage: Storage):
    """Atualiza uma tarefa existente (UPDATE)."""
    print("\n✏️  ATUALIZAR TAREFA")
    print("-" * 40)

    task_id = input("ID da tarefa: ").strip()
    task = storage.get_by_id(task_id)

    if not task:
        print(f"❌ Tarefa com ID '{task_id}' não encontrada.")
        return

    print(f"\nTarefa atual: {task.title}")
    print("Deixe em branco para manter o valor atual.\n")

    new_title = input(f"Novo título [{task.title}]: ").strip()
    if new_title:
        task.title = new_title

    new_desc = input(f"Nova descrição [{task.description}]: ").strip()
    if new_desc:
        task.description = new_desc

    print("Status: 1-A Fazer | 2-Em Progresso | 3-Concluído")
    status_input = input("Novo status (1-3): ").strip()
    status_map = {"1": TaskStatus.TODO, "2": TaskStatus.IN_PROGRESS, "3": TaskStatus.DONE}
    if status_input in status_map:
        task.status = status_map[status_input]

    print("Prioridade: 1-Baixa | 2-Média | 3-Alta")
    priority_input = input("Nova prioridade (1-3): ").strip()
    priority_map = {"1": TaskPriority.LOW, "2": TaskPriority.MEDIUM, "3": TaskPriority.HIGH}
    if priority_input in priority_map:
        task.priority = priority_map[priority_input]

    new_assignee = input(f"Novo responsável [{task.assignee}]: ").strip()
    if new_assignee:
        task.assignee = new_assignee

    task.updated_at = datetime.utcnow().isoformat()
    storage.update(task)
    print(f"\n✅ Tarefa '{task.title}' atualizada com sucesso!")


def delete_task(storage: Storage):
    """Exclui uma tarefa (DELETE)."""
    print("\n🗑️  EXCLUIR TAREFA")
    print("-" * 40)

    task_id = input("ID da tarefa: ").strip()
    task = storage.get_by_id(task_id)

    if not task:
        print(f"❌ Tarefa com ID '{task_id}' não encontrada.")
        return

    confirm = input(f"Confirma exclusão de '{task.title}'? (s/N): ").strip().lower()
    if confirm == 's':
        storage.delete(task_id)
        print(f"✅ Tarefa '{task.title}' excluída com sucesso!")
    else:
        print("Operação cancelada.")


def filter_by_status(storage: Storage):
    """Filtra tarefas por status."""
    print("\n🔍 FILTRAR POR STATUS")
    print("1-A Fazer | 2-Em Progresso | 3-Concluído")
    choice = input("Escolha (1-3): ").strip()
    status_map = {"1": TaskStatus.TODO, "2": TaskStatus.IN_PROGRESS, "3": TaskStatus.DONE}
    status = status_map.get(choice)
    if status:
        tasks = storage.get_by_status(status)
        list_tasks(storage, tasks)
    else:
        print("❌ Opção inválida.")


def filter_by_priority(storage: Storage):
    """Filtra tarefas por prioridade."""
    print("\n🔍 FILTRAR POR PRIORIDADE")
    print("1-Baixa | 2-Média | 3-Alta")
    choice = input("Escolha (1-3): ").strip()
    priority_map = {"1": TaskPriority.LOW, "2": TaskPriority.MEDIUM, "3": TaskPriority.HIGH}
    priority = priority_map.get(choice)
    if priority:
        tasks = storage.get_by_priority(priority)
        list_tasks(storage, tasks)
    else:
        print("❌ Opção inválida.")


def main():
    """Função principal do sistema."""
    storage = Storage()

    while True:
        clear_screen()
        print_header()
        print_menu()

        choice = input("\nEscolha uma opção: ").strip()

        if choice == "1":
            create_task(storage)
        elif choice == "2":
            list_tasks(storage)
        elif choice == "3":
            update_task(storage)
        elif choice == "4":
            delete_task(storage)
        elif choice == "5":
            filter_by_status(storage)
        elif choice == "6":
            filter_by_priority(storage)
        elif choice == "0":
            print("\n👋 Encerrando TaskFlow. Até logo!")
            break
        else:
            print("❌ Opção inválida. Tente novamente.")

        input("\nPressione ENTER para continuar...")


if __name__ == "__main__":
    main()
