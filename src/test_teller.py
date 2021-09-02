from unittest import mock, TestCase
import pytest

from .teller import Teller


class TestTeller(TestCase):
    @pytest.fixture(autouse=True)
    def _setup(self):
        self.cb_client = mock.MagicMock()
        self.teller = Teller(self.cb_client)

    def test_get_available_funds_no_accounts(self):
        # No accounts available
        self.cb_client.get_accounts = lambda: []
        self.assertRaises(ValueError, self.teller.get_available_funds)

    def test_get_available_funds(self):
        # Mock out accounts
        balance = 100
        accounts = [{
            'currency': 'GBP',
            'available': 0,
        },
        {
            'currency': 'USD',
            'available': balance,
        }]
        self.cb_client.get_accounts = lambda: accounts

        assert self.teller.get_available_funds() == balance

    def test_deposit_empty(self):
        assert self.teller.deposit(0) is None
        assert self.teller.deposit(-12.51) is None

    def test_deposit_no_payment_methods(self):
        self.cb_client.get_payment_methods = lambda: []

        # Do the deposit, should fail because no payment methods
        self.assertRaises(ValueError, lambda: self.teller.deposit(100))

    def test_deposit(self):
        deposit_amount = 100
        payment_method_id = 'someid'
        payment_methods = [{
            'id': payment_method_id,
            'type': 'ach_bank_account',
        }]
        self.cb_client.get_payment_methods = lambda: payment_methods

        # Do the deposit
        assert self.teller.deposit(deposit_amount) is not None

        # Make sure Coinbase Pro was called correctly
        self.cb_client.deposit.assert_called_once_with(deposit_amount, 'USD', payment_method_id)
