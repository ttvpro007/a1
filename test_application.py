import pytest
import datetime
from unittest.mock import MagicMock
from application import find_customer_by_number, process_event_history, new_month, create_customers
from customer import Customer
from phoneline import PhoneLine
from contract import Contract
from call import Call
from data import tiny_data

@pytest.fixture
def sample_customers():
    """Fixture to create sample Customer objects based on tiny_data."""
    return create_customers(tiny_data)

def test_process_event_history(sample_customers, monkeypatch):
    """Test process_event_history function using tiny_data."""
    
    # Mock new_month function to track calls
    mock_new_month = MagicMock()
    monkeypatch.setattr("application.new_month", mock_new_month)

    # Call function under test
    process_event_history(tiny_data, sample_customers)
    
    # # Ensure that new_month was called for January 2018
    # mock_new_month.assert_called_with(sample_customers, 1, 2018)

    # # Extract customers by ID for easier access
    # customer_5716 = next(c for c in sample_customers if c.customer_id == 5716)
    # customer_3895 = next(c for c in sample_customers if c.customer_id == 3895)

    # # Verify calls were registered correctly
    # assert len(customer_5716.phone_lines["422-4785"].call_history.outgoing_calls) == 1
    # assert len(customer_3895.phone_lines["136-5226"].call_history.incoming_calls) == 1

    # # Verify the call details
    # outgoing_call = customer_5716.phone_lines["422-4785"].call_history.outgoing_calls[0]
    # incoming_call = customer_3895.phone_lines["136-5226"].call_history.incoming_calls[0]

    # assert outgoing_call.duration == 117
    # assert outgoing_call.destination_number == "136-5226"
    
    # assert incoming_call.duration == 117
    # assert incoming_call.source_number == "422-4785"
