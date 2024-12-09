import pytest
from unittest import mock
import subprocess
import os
import sys

# Импортируем функции из основного скрипта
from Confmg2 import get_commit_dependencies, create_plantuml_graph

# Тест для функции get_commit_dependencies
def test_get_commit_dependencies():
    # Мокируем subprocess.check_output для имитации вывода команды git
    with mock.patch('subprocess.check_output') as mock_check_output:
        # Мокаем вывод команды git rev-list (получение хеша коммита)
        mock_check_output.return_value = b'abc1234'
        
        # Мокаем вывод команды git log (получение истории коммитов)
        # Должны быть две строки: первый коммит с родителем и второй коммит с родителем
        mock_check_output.side_effect = [
            b'abc1234 def5678 ghi91011',  # Лог с коммитами и их родителями
            b'Commit message for abc1234',  # Сообщение коммита abc1234
            b'def5678',  # Родители коммита def5678
            b'Commit message for def5678',  # Сообщение коммита def5678
            b'ghi91011',  # Родители коммита ghi91011
            b'Commit message for ghi91011',  # Сообщение коммита ghi91011
        ]
        
        # Вызываем функцию с поддельным репозиторием
        repo_path = "/fake/repo"
        dependencies = get_commit_dependencies(repo_path)
        
        # Печать для отладки
        print("Dependencies found:", dependencies)
        
        # Проверяем, что результат правильный
        assert len(dependencies) == 3
        assert dependencies[0] == ("abc1234", "Commit message for abc1234", ["def5678", "ghi91011"])
        assert dependencies[1] == ("def5678", "Commit message for def5678", [])
        assert dependencies[2] == ("ghi91011", "Commit message for ghi91011", [])


# Тест для функции create_plantuml_graph
def test_create_plantuml_graph():
    # Мокаем subprocess.run, чтобы избежать запуска реальной команды
    with mock.patch('subprocess.run') as mock_run:
        # Мокаем subprocess.check_output, чтобы не обращаться к git
        mock_check_output = mock.Mock()
        mock_check_output.return_value = b'abc1234 def5678\nghi91011'

        # Мокаем функцию для создания графа
        dependencies = [
            ("abc1234", "Commit message for abc1234", ["def5678"]),
            ("def5678", "Commit message for def5678", []),
            ("ghi91011", "Commit message for ghi91011", [])
        ]

        # Мокаем файловые операции
        with mock.patch('builtins.open', mock.mock_open()):
            with mock.patch('os.rename'):
                with mock.patch('os.remove'):
                    # Вызываем тестируемую функцию
                    create_plantuml_graph(dependencies, "output.png", "/fake/path/plantuml.jar")
                    
                    # Проверяем вызов subprocess.run
                    mock_run.assert_called_once_with(
                        ["java", "-jar", "/fake/path/plantuml.jar", "temp_graph.txt", "-tpng", "-o", ""],
                        check=True
                    )