from enum import Enum
from typing import Optional, Callable
from datetime import datetime
from task_service import TaskService


class TaskPriority(Enum):
    LOW_PRIORITY = "низкий"
    MID_PRIORITY = "средний"
    HIGH_PRIORITY = "высокий"

class TaskCategory(Enum):
    WORK = "работа"
    PERSONAL = "личное"
    STUDY = "учеба"
    HEALTH = "здоровье"
    OTHER = "прочее"

SORTING_MAP = {
    "приоритет": "priority",
    "дата окончания": "due_date",
    "категория": "category",
    "статус": "status",
}

UPDATING_MAP = {
    "название": "title",
    "описание": "description",
    "приоритет": "priority",
    "дата окончания": "due_date",
    "категория": "category",
}

SEARCHING_MAP = {
    "название и описание": "search",
    "приоритет": "priority",
    "статус": "status",
}

CANCEL_WORD = "stop"

def validate_input(
        prompt: str,
        error_message: str,
        validator: Callable[[str], bool],
        cancel_word: str = CANCEL_WORD
) -> Optional[str]:
    """
    Функция для проверки вводимых данных.
    :param prompt: Текст для описания запроса данных на ввод
    :param error_message: Текст сообщения в случае возникновении ошибки
    :param validator: Функция, проводящая валидацию.
    :param cancel_word: Слово для остановки выполнения выбранной функции
    :return: True/False или None для остановки процесса валидации.
    """
    while True:
        try:
            value = input(f"{prompt} (введите '{cancel_word}' для отмены): ")
        except UnicodeDecodeError:
            print("Ошибка декодирования ввода. Пожалуйста, попробуйте снова.")
            continue

        if value.lower() == cancel_word.lower():
            return None

        if validator(value):
            return value

        print(error_message)

def is_valid_sorting_type(value: str) -> bool:
    return value in SORTING_MAP.keys()

def is_valid_updating_type(value: str) -> bool:
    return value in UPDATING_MAP.keys()

def is_valid_searching_type(value: str) -> bool:
    return value in SEARCHING_MAP.keys()

def is_valid_status(value: str) -> bool:
    return value in ['выполнена', 'не выполнена']

def is_valid_category(value: str) -> bool:
    return value in {cat.value for cat in TaskCategory}

def is_not_empty(value: str) -> bool:
    """Проверяет, что передана не пустая строка"""
    return bool(value and value.strip())

def is_valid_date(value: str) -> bool:
    input_date = datetime.strptime(value, "%Y-%m-%d")
    current_date = datetime.today().date()
    return input_date.date() >= current_date

def is_positive_integer(value: str) -> bool:
    """Проверяет, что введенное значение - целое положительное число"""
    return value.isdigit() and int(value) >= 0

def is_valid_priority(value: str) -> bool:
    """Проверяет что введенный статус соответствует одному из доступных статусов"""
    return value in {priority.value for priority in TaskPriority}


class TaskManager:
    def __init__(self, task_service: TaskService = TaskService()):
        self.task_service = task_service

    def display_tasks(self):
        print("\nПросмотр задач: \n")
        display_options = {
            1: "Просмотр всех задачи",
            2: "Просмотр задач с сортировкой",
            3: "Просмотр задач по категориям",
            4: "Просмотр задачи по id",
        }

        for key, value in display_options.items():
            print(f"{key}. {value}")

        choice = input("\nВведите номер действия: ")
        actions = {
            "1": self.display_all_tasks,
            "2": self.display_sorted_tasks,
            "3": self.display_category_tasks,
            "4": self.display_task_by_id,
        }

        action = actions.get(choice)
        if action:
            action()
        else:
            print("\nНеверный ввод. Возвращаюсь в главное меню.\n")
            return


    def display_all_tasks(self):
        self.task_service.display_tasks()

    def display_sorted_tasks(self):
        input_sorting_term = validate_input(
            "Введите параметр сортировки ('приоритет', 'дата окончания', 'категория', 'статус')",
            "Введите корректный тип сортировки - 'приоритет', 'дата окончания', 'категория' или 'статус'",
            is_valid_sorting_type
        )
        if input_sorting_term is None:
            print("Действие отменено\n")
            return

        sorting_type = SORTING_MAP.get(input_sorting_term)
        self.task_service.display_sorted_tasks(sorting_type)

    def display_category_tasks(self):
        category = validate_input(
            "Введите нужную категорию ('работа', 'личное', 'учеба', 'здоровье', 'прочее')",
            "Некорректный ввод. Введите одну категорию -"
            " 'работа', 'личное', 'учеба', 'здоровье' или 'прочее'",
            is_valid_category
        )
        if category is None:
            print("Действие отменено\n")
            return

        self.task_service.display_tasks_by_category(category)

    def display_task_by_id(self):
        task_id = validate_input(
            "Введите ID задания",
            "ID задания должен быть целым числом",
            is_positive_integer
        )
        if task_id is None:
            print("Действие отменено\n")
            return

        self.task_service.display_single_task(int(task_id))
        return task_id

    def add_task(self):
        task = dict()

        fields = [
            ("Введите название задачи", "Название задачи не может быть пустым.", is_not_empty, "title"),
            ("Введите описание задачи", "Описание задачи не может быть пустым.", is_not_empty, "description"),
            ("Введите срок выполнения для задачи в формате 'YYYY-MM-DD' (например 2025-01-01)",
             "Срок выполнения не может быть раньше сегодняшнего дня.", is_valid_date, "due_date"),
            ("Введите категорию ('работа', 'личное', 'учеба', 'здоровье', 'прочее')",
             "Некорректный ввод. Введите одну категорию - 'работа', 'личное', 'учеба', 'здоровье' или 'прочее'",
             is_valid_category, "category"),
            ("Введите приоритет задачи ('низкий', 'средний', 'высокий')",
             "Некорректный ввод. Введите корректный приоритет - 'низкий', 'средний' или 'высокий'",
             is_valid_priority, "priority"),
        ]

        for promt, error_message, validator, key in fields:
            if (value := validate_input(promt, error_message, validator)) is None:
                print("\nДействие отменено")
                return
            task[key] = value
        self.task_service.add_task(**task)

    def modify_task(self):
        print("\nПросмотр задач: \n")
        display_options = {
            1: "Пометить задачу как выполненную",
            2: "Отредактировать задачу",
        }

        for key, value in display_options.items():
            print(f"{key}. {value}")

        choice = input("\nВведите номер действия: ")
        actions = {
            "1": self.complete_task,
            "2": self.update_task,
        }

        action = actions.get(choice)
        if action:
            action()
        else:
            print("\nНеверный ввод. Возвращаюсь в главное меню.\n")
            return

    def complete_task(self):
        task_id = self.display_task_by_id()
        self.task_service.complete_task(int(task_id))

    def update_task(self):
        task_id = self.display_task_by_id()

        update_config = {
            "название": {
                "prompt": "Введите новое название задачи",
                "error": "Название задачи не может быть пустым",
                "validator": is_not_empty,
                "field": "title"
            },
            "описание": {
                "prompt": "Введите новое описание задачи",
                "error": "Описание задачи не может быть пустым",
                "validator": is_not_empty,
                "field": "description"
            },
            "приоритет": {
                "prompt": "Введите приоритет задачи ('низкий', 'средний', 'высокий')",
                "error": "Некорректный ввод. Введите корректный приоритет - 'низкий', 'средний' или 'высокий'",
                "validator": is_valid_priority,
                "field": "priority"
            },
            "дата окончания": {
                "prompt": "Введите срок выполнения для задачи в формате 'YYYY-MM-DD' (например 2025-01-01)",
                "error": "Срок выполнения не может быть раньше сегодняшнего дня",
                "validator": is_valid_date,
                "field": "due_date"
            },
            "категория": {
                "prompt": "Введите категорию ('работа', 'личное', 'учеба', 'здоровье', 'прочее')",
                "error": "Некорректный ввод. Введите одну категорию - "
                         "'работа', 'личное', 'учеба', 'здоровье' или 'прочее'",
                "validator": is_valid_category,
                "field": "category"
            }
        }

        updating_term = validate_input(
            "Выберите поле для редактирования "
            "('название', 'описание', 'приоритет', 'дата окончания', 'категория')",
            "Введите одно название поля - "
            "'название', 'описание', 'приоритет', 'дата окончания' или 'категория'",
            is_valid_updating_type
        )
        if updating_term is None:
            print("Действие отменено\n")
            return

        field_config = update_config.get(updating_term)


        if field_config:
            new_value = validate_input(
                field_config["prompt"],
                field_config["error"],
                field_config["validator"]
            )

            if new_value is None:
                print("Действие отменено\n")
                return

            self.task_service.update_task(int(task_id), UPDATING_MAP.get(updating_term), new_value)

    def remove_task(self):
        task_id = input("Введите id задачи: ")
        self.task_service.delete_task(int(task_id))

    def search_task(self):
        ### можно искать по словам в описании или названии
        ### можно вывести все задачи с нужным нам статусом
        ### можно вывести все задачи с нужной категорией
        searching_config = {
            "название и описание": {
                "prompt": "Введите слово для поиска в названии и описании",
                "error": "Искомое слово не может быть пустым",
                "validator": is_not_empty,
                "field": "search"
            },
            "приоритет": {
                "prompt": "Введите приоритет для поиска ('низкий', 'средний', 'высокий')",
                "error": "Некорректный ввод. Введите корректный приоритет - 'низкий', 'средний' или 'высокий'",
                "validator": is_valid_priority,
                "field": "priority"
            },
            "статус": {
                "prompt": "Введите статус ('выполнена', 'не выполнена')",
                "error": "Некорректный ввод. Введите один статус - "
                         "'выполнена' или 'не выполнена'",
                "validator": is_valid_status,
                "field": "status"
            }
        }

        search_type = validate_input(
            "Выберите поле для поиска "
            "('название и описание', 'приоритет', 'статус')",
            "Введите одно название поля - "
            "'название и описание', 'приоритет' или 'статус'",
            is_valid_searching_type
        )
        if search_type is None:
            print("Действие отменено\n")
            return

        search_field = searching_config.get(search_type)
        search_term = validate_input(
            search_field["prompt"],
            search_field["error"],
            search_field["validator"]
        )
        if search_term:
            self.task_service.search_task(SEARCHING_MAP.get(search_type), search_term)

