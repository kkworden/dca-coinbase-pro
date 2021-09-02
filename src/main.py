from .config import Config
from .teller import Teller
from .purchaser import Purchaser
import time

# 6*10 = 60 seconds = 1 minute
RETRY_TIMES = 6
SLEEP_TIME_SECONDS = 10

config = Config()
teller = Teller(config.cb_client)
purchaser = Purchaser(config.cb_client)


def wait_for_funds(purchase_amt):
    """
    Waits for the specified amount of funds to be ready in the Coinbase Pro account before
    continuing. This is a blocking operation.
    :param purchase_amt: How much to purchase, in USD.
    :return: None
    """
    available_funds = teller.get_available_funds()
    tries = 0
    while available_funds < purchase_amt:
        if tries > RETRY_TIMES:
            raise ValueError(f'Insufficient funds for purchase. Needed {purchase_amt} USD '
                             f'but only {available_funds} USD was available.')

        time.sleep(SLEEP_TIME_SECONDS)
        available_funds = teller.get_available_funds()
        tries += 1

    print()
    print(f'Funds available! Will purchase {purchase_amt} USD worth of assets.')
    print()


def main():
    """
    The main function.
    :return: None
    """
    teller.deposit(config.deposit_amount)

    if config.is_deposit_only:
        print('Deposit-only mode. Exiting.')
        return
    else:
        print('Purchase mode. Will perform the following purchases:')
        print(config.purchases)

    wait_for_funds(purchaser.calculate_purchase_amount(config.purchases))
    purchaser.make_purchases(config.purchases)


def handler(event, context):
    """
    The Lambda handler function. This is the entrypoint to the application when running on AWS.
    :param event: The Lambda event.
    :param context: The Lambda context.
    :return: A Lambda response.
    """
    try:
        print('=== Starting DCA script! ===')
        main()
        print('=== Done! ===')
    except Exception as e:
        print('=== ERROR. See the logs ===')
        return {
            'message': repr(e)
        }

    return {
        'message': 'OK'
    }


# Run the main function if we're executing locally
if __name__ == '__main__':
    main()