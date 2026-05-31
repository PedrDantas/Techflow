"""
Configuração global do Pytest para o projeto TaskFlow.
Adiciona o diretório src ao PYTHONPATH para importações corretas.
"""
import sys
import os

# Adiciona /src ao path para que os testes encontrem os módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
