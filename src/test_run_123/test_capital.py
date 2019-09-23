# test_capitalize.py

import pytest

def test_capital_case():
    assert 'semaphore'.upper() == 'SEMAPHORE'

def test_int_type():
    assert type(9) is int

def test_raises_exception_on_non_string_arguments():
    assert 9 == 10

def test_input_is_equal():
    assert 9 == "9"
