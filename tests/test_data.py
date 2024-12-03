from task_service import TaskStatus

sample_tasks = [
    {
        "id": 1,
        "title": "Task 1",
        "description": "Description 1",
        "category": "работа",
        "due_date": "2023-12-01",
        "priority": "высокий",
        "status": TaskStatus.UNCOMPLETED.value,
    },
    {
        "id": 2,
        "title": "Task 2",
        "description": "Description 2",
        "category": "личное",
        "due_date": "2023-12-02",
        "priority": "средний",
        "status": TaskStatus.UNCOMPLETED.value,
    },
]
