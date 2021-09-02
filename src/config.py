import json
import boto3
import cbpro
import os


def _production_configs():
    CREDENTIALS_SECRET_NAME = os.environ['CREDENTIALS_SECRET_NAME']
    CONFIG_SECRET_NAME = os.environ['CONFIG_SECRET_NAME']

    secrets_client = boto3.client('secretsmanager')

    credentials = json.loads(secrets_client.get_secret_value(SecretId=CREDENTIALS_SECRET_NAME)['SecretString'])
    cfg = json.loads(secrets_client.get_secret_value(SecretId=CONFIG_SECRET_NAME)['SecretString'])

    return cfg, credentials


def _local_configs():
    with open('./config/local_config.json') as f:
        cfg = json.loads(f.read())

    with open('./config/local_creds.json') as f:
        credentials = json.loads(f.read())

    return cfg, credentials


class Config:
    def __init__(self):
        if 'PRODUCTION' in os.environ and os.environ['PRODUCTION'] == 'YES_PLEASE':
            cfg, credentials = _production_configs()
            print('Running in PRODUCTION mode. Credentials are pulled from AWS Secrets Manager.')
        else:  # Not production. Read from local files.
            cfg, credentials = _local_configs()
            print('Initializing client for sandbox mode. Please set PRODUCTION=1 for real clients.')

        # Get some configuration values
        self.is_deposit_only: bool = cfg['isDepositOnly']
        self.deposit_amount: float = cfg['depositAmount']
        self.purchases: list = cfg['purchases']

        # Init the client
        self.cb_client: cbpro.AuthenticatedClient = cbpro.AuthenticatedClient(credentials['key'],
                                                                              credentials['secret'],
                                                                              credentials['passphrase'],
                                                                              api_url=credentials['apiUrl'])

        # Log for clarity
        if self.is_deposit_only:
            print('Deposit-only mode. This means that funds will be deposited, but no purchase will occur.')
        else:
            print('Purchase mode. This means that funds will be deposited and purchases will be made.')

