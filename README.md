# 1. Клонирование репозитория
Склонируйте репозиторий с исходным кодом и тестами:
```
git clone <URL репозитория>
cd <директория проекта>
```

# 2. Запуск окружения
#Активируйте виртуальное окружение
```
python -m venv venv
#Для Windows:
venv\Scripts\activate
#Для MacOS/Linux:
source venv/bin/activate
pip install pytest

python __main__.py
```

# 3. Структура проекта
```
Confmg2.py           # Файл с реализацией графа зависимостей
Test.py      # Файл с тестами для команд
server.git # папка с зависимостями
```

# 4. Запуск тестов
Мы будем использовать модуль Python pytest для тестирования.
```
pytest Test.py
```
