from unittest import mock, TestCase
import pytest

from .purchaser import Purchaser


class TestPurchaser(TestCase):
    @pytest.fixture(autouse=True)
    def _setup(self):
        self.cb_client = mock.MagicMock()
        self.purchaser = Purchaser(self.cb_client)

    def test_calculate_purchase_amount_no_purchases(self):
        assert self.purchaser.calculate_purchase_amount([]) == 0

    def test_calculate_purchase_amount(self):
        purchases = [
            {'pair': 'pair1', 'amount': 100},
            {'pair': 'pair1', 'amount': 200},
        ]

        # Assert that the total purchase amount is correct
        assert self.purchaser.calculate_purchase_amount(purchases) == 300

    def test_make_purchases_no_purchases(self):
        self.purchaser.make_purchases([])

        # Should not call Coinbase Pro
        self.cb_client.place_market_order.assert_not_called()

    def test_make_purchases(self):
        purchases = [
            {'pair': 'pair1', 'amount': 100},
            {'pair': 'pair2', 'amount': 200},
        ]

        self.purchaser.make_purchases(purchases)

        # Should make the appropriate purchases
        self.cb_client.place_market_order.assert_has_calls([
            mock.call(product_id=p['pair'], side='buy', funds=str(p['amount']))
            for p in purchases
        ])
