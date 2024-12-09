import pytest
from unittest import mock
import subprocess
import os
import sys

# ����������� ������� �� ��������� �������
from Confmg2 import get_commit_dependencies, create_plantuml_graph

# ���� ��� ������� get_commit_dependencies
def test_get_commit_dependencies():
    # �������� subprocess.check_output ��� �������� ������ ������� git
    with mock.patch('subprocess.check_output') as mock_check_output:
        # ������ ����� ������� git rev-list (��������� ���� �������)
        mock_check_output.return_value = b'abc1234'
        
        # ������ ����� ������� git log (��������� ������� ��������)
        # ������ ���� ��� ������: ������ ������ � ��������� � ������ ������ � ���������
        mock_check_output.side_effect = [
            b'abc1234 def5678 ghi91011',  # ��� � ��������� � �� ����������
            b'Commit message for abc1234',  # ��������� ������� abc1234
            b'def5678',  # �������� ������� def5678
            b'Commit message for def5678',  # ��������� ������� def5678
            b'ghi91011',  # �������� ������� ghi91011
            b'Commit message for ghi91011',  # ��������� ������� ghi91011
        ]
        
        # �������� ������� � ���������� ������������
        repo_path = "/fake/repo"
        dependencies = get_commit_dependencies(repo_path)
        
        # ������ ��� �������
        print("Dependencies found:", dependencies)
        
        # ���������, ��� ��������� ����������
        assert len(dependencies) == 3
        assert dependencies[0] == ("abc1234", "Commit message for abc1234", ["def5678", "ghi91011"])
        assert dependencies[1] == ("def5678", "Commit message for def5678", [])
        assert dependencies[2] == ("ghi91011", "Commit message for ghi91011", [])


# ���� ��� ������� create_plantuml_graph
def test_create_plantuml_graph():
    # ������ subprocess.run, ����� �������� ������� �������� �������
    with mock.patch('subprocess.run') as mock_run:
        # ������ subprocess.check_output, ����� �� ���������� � git
        mock_check_output = mock.Mock()
        mock_check_output.return_value = b'abc1234 def5678\nghi91011'

        # ������ ������� ��� �������� �����
        dependencies = [
            ("abc1234", "Commit message for abc1234", ["def5678"]),
            ("def5678", "Commit message for def5678", []),
            ("ghi91011", "Commit message for ghi91011", [])
        ]

        # ������ �������� ��������
        with mock.patch('builtins.open', mock.mock_open()):
            with mock.patch('os.rename'):
                with mock.patch('os.remove'):
                    # �������� ����������� �������
                    create_plantuml_graph(dependencies, "output.png", "/fake/path/plantuml.jar")
                    
                    # ��������� ����� subprocess.run
                    mock_run.assert_called_once_with(
                        ["java", "-jar", "/fake/path/plantuml.jar", "temp_graph.txt", "-tpng", "-o", ""],
                        check=True
                    )