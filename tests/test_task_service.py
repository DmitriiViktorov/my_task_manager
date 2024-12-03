import pytest
from unittest.mock import MagicMock, patch
from data_manager import DataManager
from task_service import TaskService, TaskStatus
from test_data import sample_tasks

@pytest.fixture
def data_manager():
    data_manager = MagicMock(spec=DataManager)
    data_manager.load_tasks.return_value = sample_tasks
    return data_manager

@pytest.fixture
def task_service(data_manager):
    return TaskService(data_manager=data_manager)

def test_add_task(task_service, data_manager):
    task_service.add_task(
        title="New Task",
        description="New Description",
        category="New Category",
        due_date="2023-12-03",
        priority="низкий",
    )
    assert len(task_service.tasks) == 3
    new_task = task_service.tasks[-1]
    assert new_task.title == "New Task"
    assert new_task.status == TaskStatus.UNCOMPLETED.value
    data_manager.save_tasks.assert_called_once()

def test_delete_task(task_service, data_manager):
    with patch('builtins.input', return_value='да'):
        task_service.delete_task(1)
    assert len(task_service.tasks) == 1
    data_manager.save_tasks.assert_called_once()

def test_display_tasks(task_service, capsys):
    task_service.display_tasks()
    captured = capsys.readouterr()
    assert "Task 1" in captured.out
    assert "Task 2" in captured.out

def test_display_sorted_tasks(task_service, capsys):
    task_service.display_sorted_tasks('priority')
    captured = capsys.readouterr()
    assert "Task 1" in captured.out
    assert "Task 2" in captured.out
    assert captured.out.index("Task 1") < captured.out.index("Task 2")

def test_display_tasks_by_category(task_service, capsys):
    task_service.display_tasks_by_category("работа")
    captured = capsys.readouterr()
    assert "Task 1" in captured.out
    assert "Task 2" not in captured.out

def test_display_single_task(task_service, capsys):
    task_service.display_single_task(1)
    captured = capsys.readouterr()
    assert "Task 1" in captured.out
    assert "Description 1" in captured.out

def test_search_task(task_service, capsys):
    task_service.search_task('search', 'Task 1')
    captured = capsys.readouterr()
    assert "Task 1" in captured.out
    assert "Task 2" not in captured.out

def test_complete_task(task_service, data_manager):
    task_service.complete_task(1)
    completed_task = task_service.tasks[0]
    assert completed_task.status == TaskStatus.COMPLETED.value
    data_manager.save_tasks.assert_called_once()

def test_update_task(task_service, data_manager):
    task_service.update_task(1, 'title', 'Updated Task')
    updated_task = task_service.tasks[0]
    assert updated_task.title == 'Updated Task'
    data_manager.save_tasks.assert_called_once()

def test_get_task_by_id(task_service):
    task = task_service._get_task_by_id(1)
    assert task.title == "Task 1"
    assert task_service._get_task_by_id(999) is None

def test_sort_tasks_by_priority(task_service):
    sorted_tasks = task_service._sort_tasks_by_priority()
    assert sorted_tasks[0].id == 1
    assert sorted_tasks[1].id == 2

def test_save_tasks(task_service, data_manager):
    task_service._save_tasks()
    data_manager.save_tasks.assert_called_once()
