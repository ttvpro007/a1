"""
CSC148, Winter 2025
Assignment 1

Helper codes
"""
import datetime


# ----------------------------------------------------------------------
# Helper Functions
# ----------------------------------------------------------------------

def get_billing_date(date_str: str) -> datetime:
    """
    Convert a date string in the format "YYYY-MM-DD HH:MM:SS" into a datetime object.
    
    Parameters:
    - date_str (str): A string representing a date and time in the format "%Y-%m-%d %H:%M:%S".
    
    Returns:
    - datetime.datetime: A `datetime` object representing the parsed date and time.
    
    Example Usage:
    >>> get_billing_date("2025-02-10 14:30:00")
    datetime.datetime(2025, 2, 10, 14, 30)
    """
    return datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")