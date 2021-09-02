class Teller:
    def __init__(self, cb_client):
        self.cb_client = cb_client

    def get_available_funds(self):
        for account in self.cb_client.get_accounts():
            if account['currency'] == 'USD':
                return float(account['available'])

        raise ValueError('No USD account exists! Are you sure your account is set up properly?')

    def deposit(self, amount_usd: float):
        if amount_usd <= 0:
            print('Skipping deposit.')
            return None

        print(f'Depositing {amount_usd} funds from bank account...')

        for payment_method in self.cb_client.get_payment_methods():
            if payment_method['type'] == 'ach_bank_account':
                return self.cb_client.deposit(amount_usd, 'USD', payment_method['id'])

        raise ValueError('Could not find a ACH bank account to pull funds from...')