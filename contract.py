"""
CSC148, Winter 2025
Assignment 1

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2025 Bogdan Simion, Diane Horton, Jacqueline Smith
"""
import datetime
from math import ceil
from typing import Optional
from bill import Bill
from call import Call


# Constants for the month-to-month contract monthly fee and term deposit
MTM_MONTHLY_FEE = 50.00
TERM_MONTHLY_FEE = 20.00
TERM_DEPOSIT = 300.00

# Constants for the included minutes and SMSs in the term contracts (per month)
TERM_MINS = 100

# Cost per minute and per SMS in the month-to-month contract
MTM_MINS_COST = 0.05

# Cost per minute and per SMS in the term contract
TERM_MINS_COST = 0.1

# Cost per minute and per SMS in the prepaid contract
PREPAID_MINS_COST = 0.025
PREPAID_MIN_TOPUP_AMOUNT = 25
PREPAID_MIN_CREDIT_ALLOWED = 10


class Contract:
    """ A contract for a phone line

    This is an abstract class and should not be directly instantiated.

    Only subclasses should be instantiated.

    === Public Attributes ===
    start:
        starting date for the contract
    bill:
        bill for this contract for the last month of call records loaded from
        the input dataset
    """
    start: datetime.date
    bill: Optional[Bill]
    current_billing_date: datetime.date

    def __init__(self, start: datetime.date) -> None:
        """ Create a new Contract with the <start> date, starts as inactive
        """
        self.start = start
        self.bill = None
        self.current_billing_date = None

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ Advance to a new month in the contract, corresponding to <month> and
        <year>. This may be the first month of the contract.
        Store the <bill> argument in this contract and set the appropriate rate
        per minute and fixed cost.

        DO NOT CHANGE THIS METHOD
        """
        raise NotImplementedError

    def bill_call(self, call: Call) -> None:
        """ Add the <call> to the bill.

        Precondition:
        - a bill has already been created for the month+year when the <call>
        was made. In other words, you can safely assume that self.bill has been
        already advanced to the right month+year.
        """
        self.bill.add_billed_minutes(ceil(call.duration / 60.0))

    def cancel_contract(self) -> float:
        """ Return the amount owed in order to close the phone line associated
        with this contract.

        Precondition:
        - a bill has already been created for the month+year when this contract
        is being cancelled. In other words, you can safely assume that self.bill
        exists for the right month+year when the cancelation is requested.
        """
        self.start = None
        return self.bill.get_cost()


# TODO: Implement the MTMContract, TermContract, and PrepaidContract


class TermContract(Contract):
    end: datetime.date

    def __init__(self, start: datetime.date, end: datetime.date):
        super().__init__(start)
        self.end = end

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ Advance to a new month in the contract, corresponding to <month> and
        <year>. This may be the first month of the contract.
        Store the <bill> argument in this contract and set the appropriate rate
        per minute and fixed cost.
        """
        self.current_billing_date = datetime.date(year, month, 1)

        self.bill = bill
        self.bill.add_free_minutes(TERM_MINS)
        self.bill.add_fixed_cost(TERM_MONTHLY_FEE)
        self.bill.set_rates('TERM', TERM_MINS_COST)

        # if is first month, add term deposit cost
        if self.start.year == year and self.start.month == month:
            self.bill.add_fixed_cost(TERM_DEPOSIT)
    
    def cancel_contract(self) -> float:
        """ Return the amount owed in order to close the phone line associated
        with this contract.

        Precondition:
        - a bill has already been created for the month+year when this contract
        is being cancelled. In other words, you can safely assume that self.bill
        exists for the right month+year when the cancelation is requested.
        """
        if self.current_billing_date < self.end:
            return super().cancel_contract()
        else:
            return super().cancel_contract() - TERM_DEPOSIT


class MTMContract(Contract):

    def __init__(self, start: datetime.date):
        super().__init__(start)

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ Advance to a new month in the contract, corresponding to <month> and
        <year>. This may be the first month of the contract.
        Store the <bill> argument in this contract and set the appropriate rate
        per minute and fixed cost.
        """
        self.current_billing_date = datetime.date(year, month, 1)

        self.bill = bill
        self.bill.add_fixed_cost(MTM_MONTHLY_FEE)
        self.bill.set_rates('MTM', MTM_MINS_COST)


class PrepaidContract(Contract):
    balance: float

    def __init__(self, start: datetime.date, balance: float):
        super().__init__(start)
        self.balance = -balance

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ Advance to a new month in the contract, corresponding to <month> and
        <year>. This may be the first month of the contract.
        Store the <bill> argument in this contract and set the appropriate rate
        per minute and fixed cost.
        """
        self.current_billing_date = datetime.date(year, month, 1)

        # if there is the previous month bill
        if self.bill:
            # charge the balance of previous month's bill cost
            self.balance += self.bill.get_cost()

            # if balance is less than minimum credit allowed ($10)
            # add the minimum topup amount ($25)
            if -self.balance < PREPAID_MIN_CREDIT_ALLOWED:
                self.balance += -PREPAID_MIN_TOPUP_AMOUNT

        self.bill = bill
        self.bill.set_rates('PREPAID', PREPAID_MINS_COST)

    def cancel_contract(self) -> float:
        """ Return the amount owed in order to close the phone line associated
        with this contract.

        Precondition:
        - a bill has already been created for the month+year when this contract
        is being cancelled. In other words, you can safely assume that self.bill
        exists for the right month+year when the cancelation is requested.
        """
        # add the bill cost
        self.balance += self.bill.get_cost()

        # check balance
        if -self.balance >= 0:
            # forfeit any left over balance
            return 0
        else:
            # notify owed amount
            return self.balance

if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'datetime', 'bill', 'call', 'math'
        ],
        'disable': ['R0902', 'R0913'],
        'generated-members': 'pygame.*'
    })
