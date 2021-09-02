# Coinbase Pro Dollar Cost Averaging Lambda

### Disclaimer: This script is for educational purposes only! You are using it at your own risk!!!
____

**This script works with USD only**.

## What does this project do?
This project does 3 things:
1. Deposits money into Coinbase Pro via ACH bank account
2. Purchases cryptocurrencies on Coinbase Pro
3. (Optionally) Deploys the script to AWS Lambda for you via Terraform

This project **does not**:
1. Set up scheduling (when the script should run)
2. Take responsibility for your funds
3. Force you to use any sort of infrastructure

If you deploy to AWS, you can automatically execute the Lambda on a schedule by 
using [CloudWatch Events](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html#CronExpressions)
which is akin to cron on AWS. **Not included**.

Or, you can decide to run the script locally under a cronjob. **Not included**.

Both are excellent ways to automatically set up purchases! The reason why I didn't include
that in this project is because if you're smart enough to use this script, you probably want
to customize exactly *when* your deposits/purchases occur.

## Configuring
Configurations live in `config/`. There are 2 sets of configurations, `local` and `prod`.

`local` configurations will be loaded when you execute from your development environment.

`prod` configurations will be loaded when running as a Lambda in AWS.

Terraform will automatically copy `config/prod_config.json` and `config/prod_creds.json` to AWS
Secrets Manager. You can change the configurations in AWS Secrets Manager at any time by logging 
into the AWS console.

### Dollar cost averaging configuration
* `config/local_config.json` = if running locally
* `config/prod_config.json` = if deploying to AWS

If you only want to deposit money but NOT purchase, set `isDepositOnly` to `true`.

The script will automatically deposit `depositAmount` of USD into your Coinbase Pro account from
an ACH bank account every time the script runs. **Other deposit methods are not supported.**
Set this to `0` if you don't want to deposit anything.

You can add as many purchases as you want under the `purchases` list. **The script does not require that
the `depositAmount` add up to the amount of crypto you want to purchase**. i.e. `sum(purchases) != depositAmount` 
The script only checks if you have enough money in your Coinbase Pro account to make the purchase. If so, your
cryptocurrencies will be purchased.

### Coinbase Pro credentials
* `config/local_creds.json` = if running locally
* `config/prod_creds.json` = if deploying to AWS

You will need to set your Coinbase Pro API credentials for your account here.

## How does it work?
When you run locally with `./runapp.sh`, the app reads from the `local` config files in `config/`.
You can set your Coinbase Pro credentials, deposit amount, and coins you wish to purchase in the 
`config/local_*.json` files.

When you deploy to AWS, the `config/prod_*.json` files are copied into AWS Secrets Manager. The source code
in `src/` and the Python dependencies for the Pipenv virtualenv are zipped into an archive and uploaded to S3.
Note that the Lambda will NOT run on its own when you deploy via Terraform.

## Running locally

### Prerequisites
You will need to install:

* Python3
* Pipenv

Once installed, run:

```
pipenv install
```

### Run the app (locally)
Execute:

```
./runapp.sh
```

### Unit tests
Execute:

```
./runtests.sh
```

## Deploying to AWS Lambda

### Prerequisites
You will need to install the AWS CLI and set up [credentials in your environment](https://docs.aws.amazon.com/sdk-for-java/v1/developer-guide/setup-credentials.html).

You will also need to [install Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli).

### Deploying
The Terraform files live in `terraform/`. To deploy everything, simply do:

```
cd terraform
terraform init
terraform plan
terraform apply
```

This will deploy:
1. (1) S3 bucket
2. (1) S3 object containing source code
3. (1) IAM execution role
4. (2) AWS Secret Manager secrets for configuration
5. (1) Lambda function

Note that when you do this, **the script will NOT run automatically.** You must set up your own scheduling.

### Teardown
```
cd terraform
terraform plan -destroy
terraform apply -destroy
```