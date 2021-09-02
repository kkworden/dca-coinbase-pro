class Purchaser:
    def __init__(self, cb_client):
        self.cb_client = cb_client

    def calculate_purchase_amount(self, purchases: list):
        '''
        Calculates how much USD is needed to make all of the configured purchases.
        :return: USD, as a float, that is needed for this purchase.
        '''
        return sum([purchase['amount'] for purchase in purchases])

    def make_purchases(self, purchases: list):
        '''
        Makes purchases based on the configuration. Does NOT check if there are sufficient
        funds for purchase.
        '''
        for purchase in purchases:
            # Purchase has a 'pair' (str) key and an 'amount' (float) key
            pair = purchase['pair']
            amount_usd = purchase['amount']

            # Place a market order
            print(f'Placing market order for {amount_usd} USD of {pair}...')
            self.cb_client.place_market_order(product_id=pair, side='buy', funds=str(amount_usd))
