import pytest
from llm import generate_sql

def test_generate_sql():
    query = "Show all customers"
    sql = generate_sql(query)
    assert "SELECT" in sql  # SQL має містити SELECT
    assert "customers" in sql  # Має звертатись до таблиці customers
