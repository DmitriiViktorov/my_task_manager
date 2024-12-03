from unittest.mock import patch
from task_manager import (
    validate_input,
    is_valid_sorting_type,
    is_valid_updating_type,
    is_valid_searching_type,
    is_valid_status,
    is_valid_category,
    is_not_empty,
    is_valid_date,
    is_positive_integer,
    is_valid_priority
)


def test_validate_input():
    with patch('builtins.input', return_value='valid_input'):
        assert validate_input("Prompt", "Error", lambda x: x == 'valid_input') == 'valid_input'

    with patch('builtins.input', side_effect=['invalid_input', 'valid_input']):
        assert validate_input("Prompt", "Error", lambda x: x == 'valid_input') == 'valid_input'

    with patch('builtins.input', return_value='stop'):
        assert validate_input("Prompt", "Error", lambda x: x == 'valid_input', cancel_word='stop') is None

def test_is_valid_sorting_type():
    assert is_valid_sorting_type("приоритет") == True
    assert is_valid_sorting_type("invalid") == False

def test_is_valid_updating_type():
    assert is_valid_updating_type("название") == True
    assert is_valid_updating_type("invalid") == False

def test_is_valid_searching_type():
    assert is_valid_searching_type("название и описание") == True
    assert is_valid_searching_type("invalid") == False

def test_is_valid_status():
    assert is_valid_status("выполнена") == True
    assert is_valid_status("invalid") == False

def test_is_valid_category():
    assert is_valid_category("работа") == True
    assert is_valid_category("invalid") == False

def test_is_not_empty():
    assert is_not_empty("not empty") == True
    assert is_not_empty("") == False

def test_is_valid_date():
    assert is_valid_date("2025-12-01") == True
    assert is_valid_date("2020-01-01") == False

def test_is_positive_integer():
    assert is_positive_integer("123") == True
    assert is_positive_integer("-123") == False

def test_is_valid_priority():
    assert is_valid_priority("низкий") == True
    assert is_valid_priority("invalid") == False