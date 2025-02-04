# Менеджер задач

Этот проект представляет собой простую систему управления менеджером задач, 
которая позволяет добавлять, удалять, искать и отображать задачи, 
а также изменять их и отмечать как выполненные.

## Содержание

- [Установка](#установка)
- [Использование](#использование)
- [Тестирование](#тестирование)
- [Структура проекта](#структура-проекта)
- [Контактная информация](#контактная-информация)

## Установка

1. Клонируйте репозиторий:
    ```sh
    git clone https://github.com/DmitriiViktorov/my_task_manager.git
    cd my_task_manager
    ```

2. Для тестирования проекта необходимо выполнить установку библиотеки pytest
   ```bash
   pip install pytest

## Использование

1. Запустите основной скрипт:
    ```sh
    python main.py
    ```

2. Следуйте инструкциям на экране для выполнения различных действий:
    - Просмотр задач
    - Добавление задач
    - Выполнить/изменить задачу
    - Удалить задачу
    - Поиск задач
    - Выйти

    Приложение будет запрашивать необходимые данные для различных действий. В случае если вы ввели 
    пустое или недопустимое значение - вы увидите уведомление об этом. 
    Вы можете отменить выполнение любого действия, если введете слово 'stop'.

## Тестирование
Тесты для всего проекта находятся в отдельной директории tests.

Для запуска тестов используйте команду:
   ```bash
   pytest tests/
   ```

Вы можете выполнить тестирование каждого файла по отдельности, если это необходимо. 
Для этого необходимо будет указать имя конкретного теста, например:

   ```bash
   pytest tests/test_task_manager.py
   ```

## Структура проекта

    my_task_manager/
    ├── tests
    │   ├── conftest.py
    │   ├── test_data.py
    │   ├── test_task_service.py
    │   ├── test_task_manager_validators.py
    │   └── test_task_manager.py
    ├── data_manager.py
    ├── task_service.py
    ├── task_manager.py
    ├── main.py
    ├── tests.py
    └── README.md

- `data_manager.py`: Модуль для управления данными задач (сохранение и загрузка из файла).
- `task_service.py`: Модуль для обработки данных о задачах и взаимодействия с менеджером данных.
- `task_manager.py`: Модуль для взаимодействия между пользователем и объектом `Task`.
- `main.py`: Основной скрипт для запуска приложения.
- `tests`: Тесты для модулей `data_manager`, `task_service` и `task_manager` и файл конфигураций.
- `README.md`: Документация проекта.


## Контактная информация

В случае возникновения вопросов, комментариев, замечаний по работе приложения вы можете связаться со мной:
- Email: viktorovokrl@gmail.com
- Github: https://github.com/DmitriiViktorov
- Telegram: https://t.me/ViktorovDV
