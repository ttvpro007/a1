import pytest
from data import tiny_data  # Import tiny_data from data.py
from application import create_customers, import_data, process_event_history, Customer

@pytest.fixture
def sample_customers():
    """Fixture to create sample Customer objects based on tiny_data."""

    return create_customers(tiny_data)

if __name__ == '__main__':
    input_dictionary = import_data()
    customers = create_customers(input_dictionary)
    process_event_history(input_dictionary, customers)
