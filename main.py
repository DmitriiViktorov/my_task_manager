import sys
from task_manager import TaskManager
import io
import sys


def configure_io() -> None:
    """Настройка ввода-вывода для поддержки UTF-8"""
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def display_menu() -> None:
    """Отображает меню действий"""

    menu_items = {
        1: "Просмотр задач",
        2: "Добавить задачу",
        3: "Выполнить/изменить задачу",
        4: "Удалить задачи",
        5: "Поиск задач",
        6: "Выйти из приложения"
    }
    for key, value in menu_items.items():
        print(f"{key}. {value}")


def main() -> None:
    configure_io()
    task_manager = TaskManager()
    while True:
        display_menu()
        choice = input("\nВведите номер действия: ")

        actions = {
            "1": task_manager.display_tasks,
            "2": task_manager.add_task,
            "3": task_manager.modify_task,
            "4": task_manager.remove_task,
            "5": task_manager.search_task,
        }

        if choice == "6":
            print("\nДо свидания! Ждем вас снова в нашем менеджере задач!")
            break

        action = actions.get(choice)

        if action:
            action()
        else:
            print("\nНеверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
