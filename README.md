# 📋 TaskFlow – Sistema de Gerenciamento de Tarefas Ágeis

> Projeto desenvolvido para a disciplina de Engenharia de Software | TechFlow Solutions

![CI Pipeline](https://github.com/SEU_USUARIO/taskflow/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 🎯 Objetivo

O **TaskFlow** é um sistema de gerenciamento de tarefas baseado em metodologias ágeis, desenvolvido para atender uma startup de logística que necessita acompanhar fluxos de trabalho em tempo real, priorizar tarefas críticas e monitorar o desempenho da equipe.

---

## 📦 Escopo do Projeto

### Escopo Inicial
O sistema contempla:
- ✅ CRUD completo de tarefas (Criar, Listar, Atualizar, Excluir)
- ✅ Classificação por **status**: A Fazer, Em Progresso, Concluído
- ✅ Classificação por **prioridade**: Baixa, Média, Alta
- ✅ Atribuição de responsáveis por tarefa
- ✅ Persistência de dados em arquivo JSON
- ✅ Testes automatizados com Pytest
- ✅ Pipeline de CI/CD com GitHub Actions

### 🔄 Mudança de Escopo (Sprint 3)

**Justificativa:** Durante o desenvolvimento, o cliente (startup de logística) solicitou a adição de um **sistema de notificações por e-mail** para alertar responsáveis quando uma tarefa de alta prioridade fosse criada ou atualizada. Essa funcionalidade não estava prevista no escopo inicial, mas foi identificada como crítica para a operação da equipe.

**Impacto:** Foi adicionado o módulo `notifier.py` em `/src`, com envio de alertas via SMTP, e os respectivos testes em `/tests/test_notifier.py`. O Kanban foi atualizado com os novos cards na coluna "To Do".

---

## 🛠️ Metodologia

O projeto adota uma abordagem **híbrida Scrum + Kanban**:

- **Sprints de 1 semana** para planejamento e entrega incremental
- **Quadro Kanban** no GitHub Projects para visibilidade do fluxo
- **Commits semânticos** para rastreabilidade das mudanças
- **Code review** simulado via Pull Requests
- **CI/CD** automatizado com GitHub Actions

---

## 🗂️ Estrutura de Diretórios

```
taskflow/
├── .github/
│   └── workflows/
│       └── ci.yml          # Pipeline de CI/CD
├── src/
│   ├── app.py              # Ponto de entrada principal
│   ├── models.py           # Modelos de dados (Task, Enums)
│   └── storage.py          # Camada de persistência JSON
├── tests/
│   ├── test_models.py      # Testes unitários dos modelos
│   └── test_storage.py     # Testes unitários do storage
├── docs/
│   └── diagrams/           # Diagramas UML do projeto
├── data/                   # Armazenamento local (gerado em runtime)
├── conftest.py             # Configuração global do Pytest
├── requirements.txt        # Dependências do projeto
└── README.md               # Este arquivo
```

---

## ▶️ Como Executar

### Pré-requisitos
- Python 3.10 ou superior
- pip

### Instalação

```bash
# Clone o repositório
git clone https://github.com/SEU_USUARIO/taskflow.git
cd taskflow

# Instale as dependências
pip install -r requirements.txt
```

### Executar o sistema

```bash
python src/app.py
```

### Executar os testes

```bash
# Todos os testes
pytest tests/ -v

# Com cobertura de código
pytest tests/ --cov=src --cov-report=term-missing
```

---

## 🤖 Pipeline de CI/CD

O projeto usa **GitHub Actions** com dois jobs:

| Job | Descrição |
|-----|-----------|
| `test` | Executa todos os testes com Pytest (Python 3.10 e 3.11) |
| `lint` | Verifica qualidade do código com Flake8 |

O pipeline é acionado automaticamente em todo `push` para `main`/`develop` e em `pull requests`.

---

## 📊 Funcionalidades

| Funcionalidade | Status |
|---|---|
| Criar tarefa | ✅ Implementado |
| Listar tarefas | ✅ Implementado |
| Atualizar tarefa | ✅ Implementado |
| Excluir tarefa | ✅ Implementado |
| Filtrar por status | ✅ Implementado |
| Filtrar por prioridade | ✅ Implementado |
| Notificações por e-mail | 🔄 Em Progresso (mudança de escopo) |

---

## 👥 Equipe

- **Desenvolvedor / Gestor de Projetos:** pedro dantas
- **Empresa:** TechFlow Solutions
- **Cliente:** Startup de Logística

---
## Mudança de Escopo
Adicionado módulo de notificações por e-mail na Sprint 3.

---

## 📝 Licença

Este projeto está sob a licença MIT.
