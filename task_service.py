from dataclasses import dataclass
from enum import Enum
from typing import Any
from operator import attrgetter

from data_manager import DataManager


class TaskStatus(Enum):
    COMPLETED = "выполнена"
    UNCOMPLETED = "не выполнена"


@dataclass
class Task:
    """
    Класс Задача для упрощения манипулирования объектами задач - получения (from_dict) и
    передачи (to_dict) данных о задаче.
    """
    id: int
    title: str
    description: str
    category: str
    due_date: str
    priority: str
    status: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "due_date": self.due_date,
            "priority": self.priority,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Task':
        return cls(**data)


def require_task(func):
    def wrapper(self, task_id, *args, **kwargs):
        task = self._get_task_by_id(task_id)
        if task is None:
            return
        return func(self, task, *args, **kwargs)
    return wrapper


class TaskService:
    """
    Класс для обработки данных о задачах и взаимодействия с менеджером данных
    """
    def __init__(self, data_manager: DataManager = DataManager()):
        self.data_manager = data_manager
        self.tasks: list[Task] = [Task.from_dict(task) for task in self.data_manager.load_tasks()]

    @staticmethod
    def print_tasks(tasks: list[Task]) -> None:
        """Выводит на экран информацию о переданных заданиях"""
        if not tasks:
            print("\nЗадания не найдены.")
            return

        print(f"\n{'ID':<5}{'Название':<25}{'Описание':<45}{'Категория':<15}"
              f"{'Срок выполнения':<20}{'Приоритет':<15}{'Статус':<20}")
        print("-" * 140)
        for task in tasks:
            title = task.title if len(task.title) <= 20 else task.title[:17] + '...'
            descr = task.description if len(task.description) <= 40 else task.description[:32] + '...'
            print(
                f"{task.id:<5}{title:<25}{descr:<45}{task.category:<15}"
                f"{task.due_date:<20}{task.priority:<15}{task.status:<20}")
        print("-" * 140, '\n')

    @staticmethod
    def print_single_task(task: Task) -> None:
        """Выводит на экран информацию о выбранном задании"""
        print(f"\nЗадание {task.id}")
        for task_attr, task_value in task.to_dict().items():
            print(f"    {task_attr}: {task_value}")
        print("")


    def _sort_tasks_by_priority(self) -> list[Task]:
        """Метод для вывода заданий с корректной сортировкой по приоритету"""
        priority_weight = {
            "низкий": 1,
            "средний": 2,
            "высокий": 3
        }
        sorted_tasks = sorted(self.tasks, key=lambda task: priority_weight.get(task.priority, 0), reverse=True)
        return sorted_tasks

    def _save_tasks(self) -> None:
        """Передает список всех текущих задач в менеджер данных для сохранения."""
        self.data_manager.save_tasks([task.to_dict() for task in self.tasks])


    def _get_task_by_id(self, task_id: int) -> Task | None:
        """Ищет задачу по переданному id, в случае успеха возвращает объект Task, в противном случае возвращает None"""
        task = next((task for task in self.tasks if task.id == task_id), None)

        if not task:
            print(f"\nЗадача с таким id - '{task_id}' не найдена.\n")
            return None

        return task

    def add_task(
            self,
            title: str,
            description: str,
            category: str,
            due_date: str,
            priority: str,
    ) -> None:
        """
        Метод для добавления нового задания в базу данных.
        Присваивает задаче новый уникальный id, устанавливает статус 'не выполнена'.
        :param title: Название задачи
        :param description: Описание задачи
        :param category: Категория задача
        :param due_date: Дедлайн (срок выполнения задачи)
        :param priority: Приоритет
        """
        task_id = 1 if not self.tasks else max(task.id for task in self.tasks) + 1

        new_task = Task(
            id=task_id,
            title=title,
            description=description,
            category=category,
            due_date=due_date,
            priority=priority,
            status=TaskStatus.UNCOMPLETED.value,
        )

        self.tasks.append(new_task)
        self._save_tasks()

        print(f"\nЗадача '{new_task.title}' сохранена!")

    @require_task
    def delete_task(self, task: int | Task) -> None:
        """
        Удаляет задачу с переданным id.
        Декоратор ищет задачу по полученному id и в случае успеха возвращает в метод объект Task
        :param task: Задача, полученная от декоратора require_task.
        """
        confirm = input(f"Вы уверены, что хотите удалить задачу {task.title} с ID {task.id} (да/нет): ")
        if confirm.lower() in ('да', 'yes', 'д', 'y'):
            self.tasks.remove(task)
            self._save_tasks()
            print(f"\nЗадача с id '{task.id}' удалена.")
            return
        else:
            print(f"Удаление задачи '{task.title}' отменено.")

    def display_tasks(self) -> None:
        """Выводит на экран все задачи в порядке увеличения id."""
        if not self.tasks:
            print("В настоящие момент нет ни одной задачи.")
        self.print_tasks(self.tasks)

    def display_sorted_tasks(self, sorting_term: str) -> None:
        """Выводит на экран все задачи, отсортированные по переданному параметру."""
        if sorting_term == 'priority':
            sorted_tasks = self._sort_tasks_by_priority()
        else:
            sorted_tasks = sorted(self.tasks, key=attrgetter(sorting_term))
        self.print_tasks(sorted_tasks)

    def display_tasks_by_category(self, category: str) -> None:
        """Выводит на экран все задачи выбранной категории."""
        sorted_tasks = list(filter(lambda task: task.category == category, self.tasks))
        self.print_tasks(sorted_tasks)

    @require_task
    def display_single_task(self, task: int | Task) -> None:
        self.print_single_task(task)

    def search_task(self, search_type: str, search_term: str) -> None:
        """
        Проводит поиск среди всех задач по выбранному параметру и значению поиска.
        В случае, если есть несколько задач, удовлетворяющих критериям поиска - выводит все эти задачи.
        :param search_type: Параметр поиска.
        :param search_term: Значение для поиска по выбранному параметру.
        :return:
        """
        search_fields = {
            'search': ['title', 'description'],
            'status': ['status'],
            'priority': ['priority'],
        }
        fields = search_fields.get(search_type)
        tasks = [
            task for task in self.tasks
            if any(
                (field in ['status', 'priority'] and search_term.lower() == str(getattr(task, field)).lower()) or
                (field in ['title', 'description'] and search_term.lower() in str(getattr(task, field)).lower())
                for field in fields
            )
        ]
        if tasks:
            print("\nВот что удалось найти по вашему запросу:\n")
        self.print_tasks(tasks)

    @require_task
    def complete_task(self, task: int | Task) -> None:
        """Отмечает выбранную задачу как выполненную."""
        if task.status == TaskStatus.COMPLETED.value:
            print(f"\nЭта задача - '{task.title}' уже выполнена.\n")
            return

        task.status = TaskStatus.COMPLETED.value
        self._save_tasks()
        print(f"\nЗадача '{task.title}' выполнена!\n")

    @require_task
    def update_task(self, task: int | Task, updated_attr: str, new_value: str) -> None:
        """
        Проводит обновление выбранной задачи.
        Получает для обработки объект Task, атрибут, который необходимо изменить, и новое значение этого атрибута.
        :param task: Задача, полученная от декоратора require_task.
        :param updated_attr: Атрибут объекта Task, который надо обновить.
        :param new_value: Новое значение для атрибута Task.
        """
        setattr(task, updated_attr, new_value)
        self._save_tasks()
        print(f"\nЗадача '{task.title}' обновлена!")


