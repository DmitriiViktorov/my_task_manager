import pytest
from unittest.mock import MagicMock, patch
from task_manager import TaskManager
from task_service import TaskService, Task
from test_data import sample_tasks


@pytest.fixture
def task_service():
    task_service = MagicMock(spec=TaskService)
    task_service.tasks = [Task.from_dict(task) for task in sample_tasks]
    return task_service

@pytest.fixture
def task_manager(task_service):
    return TaskManager(task_service=task_service)

def test_display_tasks(task_manager, capsys):
    with patch('builtins.input', return_value='1'):
        task_manager.display_tasks()
    captured = capsys.readouterr()
    assert "Просмотр всех задач" in captured.out

def test_display_all_tasks(task_manager):
    with patch.object(task_manager.task_service, 'display_tasks') as mock_display_tasks:
        task_manager.display_all_tasks()
        mock_display_tasks.assert_called_once()

def test_display_sorted_tasks(task_manager, capsys):
    with patch('builtins.input', return_value='приоритет'):
        with patch.object(task_manager.task_service, 'display_sorted_tasks') as mock_display_tasks:
            task_manager.display_sorted_tasks()
            mock_display_tasks.assert_called_once()

def test_display_category_tasks(task_manager, capsys):
    with patch('builtins.input', return_value='работа'):
        with patch.object(task_manager.task_service, 'display_tasks_by_category') as mock_display_category_tasks:
            task_manager.display_category_tasks()
            mock_display_category_tasks.assert_called_once()

def test_display_task_by_id(task_manager, capsys):
    with patch('builtins.input', return_value='1'):
        with patch.object(task_manager.task_service, 'display_single_task') as mock_display_task_by_id:
            task_manager.display_task_by_id()
            mock_display_task_by_id.assert_called_once()

def test_add_task(task_manager):
    with patch('builtins.input', side_effect=['Task 3', 'Description 3', '2025-12-03', 'здоровье', 'низкий']):
        task_manager.add_task()
    task_manager.task_service.add_task.assert_called_once_with(
        title='Task 3',
        description='Description 3',
        category='здоровье',
        due_date='2025-12-03',
        priority='низкий'
    )

def test_modify_task(task_manager, capsys):
    with patch('builtins.input', side_effect=['1', '1']):
        task_manager.modify_task()
    captured = capsys.readouterr()
    assert "Пометить задачу как выполненную" in captured.out

def test_update_task(task_manager):
    with patch('builtins.input', side_effect=['1', 'название', 'New Title']):
        task_manager.update_task()
    task_manager.task_service.update_task.assert_called_once_with(1, 'title', 'New Title')

def test_remove_task(task_manager):
    with patch('builtins.input', return_value='1'):
        task_manager.remove_task()
    task_manager.task_service.delete_task.assert_called_once_with(1)

def test_search_task(task_manager, capsys):
    with patch('builtins.input', side_effect=['название и описание', 'Task']):
        task_manager.search_task()
    task_manager.task_service.search_task.assert_called_once_with(
        'search', 'Task',
    )
