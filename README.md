## Setup dependencies
### uv installation
###### macOS and Linux
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

###### Windows
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### syncing project
```bash
uv sync
```

## Project tree
```bash
┌── config
│   ├──	midddleware
│   │   ├── __init__.py
│   │   ├── audit_middleware.py
│   ├── asgi.py
│   ├── db_routers.py
│   ├── routing.py
│   ├── schema.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── apps
│   ├── analytics
│   │   ├── migrations
│   │   │   ├── __init__.py
│   │   ├── services
│   │   │   ├── __init__.py
│   │   │   ├── summary_reader.py
│   │   ├── sql
│   │   │   ├── investment_summary.sql
│   │   ├── models.py
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── admin.py
│   │   ├── tests.py
│   │   ├── views.py
│   ├── integrations
│   │   ├── migrations
│   │   │   ├── __init__.py
│   │   ├── contracts
│   │   │   ├── __init__.py
│   │   │   ├── settlement.py
│   │   ├── exchange
│   │   │   ├── __init__.py
│   │   │   ├── providers.py
│   │   ├── models.py
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── exchange_providers.py
│   │   ├── admin.py
│   │   ├── tests.py
│   │   ├── views.py
│   ├── investments
│   │   ├── migrations
│   │   │   ├── __init__.py
│   │   │   ├── 0002_rename_currrent_value_userinvestment_current_value.py
│   │   ├── ml
│   │   │   ├── __init__.py
│   │   │   ├── fraud_detector.py
│   │   │   ├── train_model.py
│   │   ├── services
│   │   │   ├── __init__.py
│   │   │   ├── cached_investment_service.py
│   │   │   ├── matching_engine.py
│   │   │   ├── statement_service.py
│   │   │   ├── yield_calculation_service.py
│   │   ├── utils
│   │   │   ├── __init__.py
│   │   │   ├── notification.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── __init__.py
│   │   ├── validators.py
│   │   ├── tasks.py
│   │   ├── schema.py
│   │   ├── routing.py
│   │   ├── pagination.py
│   │   ├── consumers.py
│   │   ├── constants.py
│   │   ├── apps.py
│   │   ├── admin.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   ├── views.py
│   ├── notifications
│   │   ├── migrations
│   │   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── events.py
│   │   ├── admin.py
│   │   ├── tests.py
│   │   ├── views.py
│   ├── users
│   │   ├── migrations
│   │   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── permissions.py
│   │   ├── admin.py
│   │   ├── tests.py
│   │   ├── views.py
│   ├── wallets
│   │   ├── migrations
│   │   │   ├── __init__.py
│   │   ├── services
│   │   │   ├── __init__.py
│   │   │   ├── exchange_service.py
│   │   │   ├── reconciliation_service.py
│   │   │   ├── transaction_engine.py
│   │   ├── utils
│   │   │   ├── __init__.py
│   │   │   ├── notifications.py
│   │   ├── models.py
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── tasks.py
│   │   ├── admin.py
│   │   ├── tests.py
│   │   ├── views.py
├── pyproject.toml
├── db.sqlite3
├── README.md
├── insomnia-collection.yaml
├── Dockerfile
├── docker-comspose.django.yml
├── docker-comspose.postgre.yml
├── docker-comspose.redis.yml
├── .gitignore
├── .python-version
├── .env-example
├── manage.py
└── uv.lock
```

## Run project utilities 
### runserver
```bash
uv run manage.py runserver
```

### makemigrations
```bash
uv run manage.py makemigrations
```

### migrate
```bash
uv run manage.py migrate
```

### dephne
```bash
uv run dephne config.asgi.application
```

### celery | worker
```bash
uv run celery -A config worker -l info
```

### celery | beat
```bash
uv run celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

## Deployment orchestration
### build image
```bash
docker build -t orchest-investment:1.0.0 .
```

### upstream redis
```bash
docker compose -f docker-compose.redis.yml up -d
```

### upstream postgre
```bash
docker compose -f docker-compose.postgre.yml up -d
```

### run project
```bash
docker compose -f docker-compose.django.yml up -d
```

## API Guidance
### Get token
###### POST /api/v1/token/
#### *payload*
```json
{
    "username": "admin",
    "password": "admin"
}
```
#### *response*
```json
{
    "refresh": "<token>",
    "access": "<token>"
}
```

### Get refresh token
###### POST /api/v1/token/refresh/
#### *payload*
```json
{
    "refresh": "<token>"
}
```
#### *response*
```json
{
    "access": "<token>"
}
```

### Get investment list
###### GET /api/v1/investments/
#### *Authorization*
```bash
Bearer <access_token>
```
#### *response*
```json
{
    "count": 11,
    "next": "http://127.0.0.1:8000/api/v1/investments/?page=2",
    "results": [
        {
            "id": 7,
            "asset_name": "Wine Investment B",
            "amount_invested": "2800.00",
            "current_value": "2850.00",
            "profit_loss": "50.00",
            "profit_loss_percentage": "1.79",
            "purchase_date": "2024-03-28T10:00:00Z"
        }
    ]
}
```

### Create investment
###### POST /api/v1/investments/
#### *Authorization*
```bash
Bearer <access_token>
```
#### *payload*
```json
{
    "asset_name": "Healthcare ETF",
    "amount_invested": "2200.00",
    "purchase_date": "2024-03-02T10:00:00Z",
    "current_value": "2100.00",
    "is_active": true
}
```
#### *response*
```json
{
    "asset_name": "Healthcare ETF",
    "amount_invested": "2200.00",
    "purchase_date": "2024-03-02T10:00:00Z",
    "current_value": "2100.00",
    "is_active": true,
    "profit_loss": "-100.00",
    "profit_loss_percentage": "-4.55"
}
```

### Investment summary
###### GET /api/v1/investments/summary/
#### *Authorization*
```bash
Bearer <access_token>
```
#### *response*
```json
{
    "total_invested": "416000",
    "current_value": "132900",
    "total_profit_loss": "-283100",
    "active_investments": 4,
    "best_performing": "Tesla Model 3",
    "worst_performing": "Bayerische Motoren Werke M3",
    "portfolio_roi_percentage": -68.05,
    "insights": {
        "average_holding_period_days": 1238,
        "average_investment_size": 104000
    }
}
```

### Investment summary
###### POST /api/v1/investment/bulk-create/
#### *Authorization*
```bash
Bearer <access_token>
```
#### *response*
```json
[
    {
        "asset_name": "Tesla",
        "amount_invested": "2000.00",
        "purchase_date": "2024-01-10T00:00:00Z",
        "current_value": "2100.00",
        "is_active": true,
        "currency": 1
	},
    {
        "asset_name": "Apple",
        "amount_invested": "3000.00",
        "purchase_date": "2024-01-20T00:00:00Z",
        "current_value": "3200.00",
        "is_active": true,
        "currency": 1
    }
]
```

## GraphQL Guidance
### Authenication
###### mutation | tokenAuth
```graphql
mutation {
    tokenAuth(username: "admin", password: "admin") {
        token
        refreshToken
        payload {
            username
        }
    }
}
```
###### response
```json
{
    "data": {
        "tokenAuth": {
            "token": "<access_token>",
            "refreshToken": "<refresh_token>",
            "payload": {
                "username": "admin"
            }
        }
    }
}
```

###### mutation | refreshToken
```graphql
mutation {
    refreshToken(refreshToken: "<token>") {
        token
    }
}
```
###### response
```json
{
    "data": {
        "refreshToken": {
            "token": "<new_access_token>"
        }
    }
}
```

### Create Investment
###### mutation | createInvestment
```graphql
mutation {
    createInvestment(input: {
        assetName: "Gold",
        amountInvested: "5000.00",
        purchaseDate: "2024-04-01T00:00:00Z",
        currentValue: "5100.00",
        isActive: true,
        currencyId: 1,
        yieldRate: "5.00"
    }) {
        investment {
            id
            assetName
            profitLoss
            profitLossPercentage
        }
    }
}

```
###### response
```json
{
    "data": {
        "createInvestment": {
            "investment": {
                "id": 8,
                "assetName": "Gold",
                "profitLoss": "100.00",
                "profitLossPercentage": "2.00"
            }
        }
    }
}
```

### Investment Summary
###### query | investmentSummary
```graphql
query {
    investmentSummary {
        totalInvested
        totalValue
        totalProfitLoss
        activeInvestments
        bestPerforming
        worstPerforming
        portfolioRoiPercentage
        insights {
            averageHoldingPeriodDays
            averageInvestmentSize
        }
    }
}
```
###### response
```json
{
    "data": {
        "investmentSummary": {
            "totalInvested": "416000.00",
            "totalValue": "132900.00",
            "totalProfitLoss": "-283100.00",
            "activeInvestments": 4,
            "bestPerforming": "Tesla Model 3",
            "worstPerforming": "BMW M3",
            "portfolioRoiPercentage": -68.05,
            "insights": {
                "averageHoldingPeriodDays": 1238,
                "averageInvestmentSize": 104000.00
            }
        }
    }
}
```

### List All Investment
###### query | investment
```graphql
query {
    investments {
        id
        assetName
        amountInvested
        currentValue
        profitLoss
        profitLossPercentage
        purchaseDate
        isActive
        currency {
            code
            network
        }
    }
}
```
###### response
```json
{
    "data": {
        "investments": [
            {
                "id": 1,
                "assetName": "Tesla Model 3",
                "amountInvested": "50000.00",
                "currentValue": "52500.00",
                "profitLoss": "2500.00",
                "profitLossPercentage": "5.00",
                "purchaseDate": "2024-01-15T10:00:00Z",
                "isActive": true,
                "currency": {
                    "code": "USDT",
                    "network": "ERC20"
                }
            }
        ]
    }
}
```

### Get Investment by ID
###### query | investment(id: ID!)
```graphql
query {
    investment(id: 1) {
        id
        assetName
        amountInvested
        currentValue
        profitLoss
        profitLossPercentage
        purchaseDate
        isActive
        currency {
            code
        }
    }
}
```

### List Yield Payments
###### query | yieldPayment
```graphql
query {
    yieldPayments {
        id
        amount
        currency {
            code
        }
        paymentDate
        transactionHash
        status
        investment {
            assetName
        }
    }
}
```

### List User Wallets
###### query | wallets
```graphql
query {
    wallets {
        id
        address
        balance
        lockedBalance
        currency {
            code
            network
        }
    }
}
```

### List Available Currencies 
###### query | currencies
```graphql
query {
    currencies {
        id
        code
        network
        contractAddress
        decimalPlaces
    }
}
```

## GraphQL Guidance for Blockchain
### All Block
###### query | allBlocks
```graphql
query {
    allBlocks
}
```
###### response
```json
{
    "data": {
        "allBlocks": "[{\"hash\": \"e24d032c5906e35f8da2ff39ccde24df3d4b23ea9d609df7f65522e0a9cba946\", \"index\": 0, \"prev_hash\": \"0\", \"timestamp\": 1750000581506, \"transactions\": []}]"
    }
}
```

### Latest Block
###### query | latestBlock
```graphql
query {
    latestBlock
}
```
###### response
```json
{
    "data": {
        "latestBlock": "{\"hash\": \"e24d032c5906e35f8da2ff39ccde24df3d4b23ea9d609df7f65522e0a9cba946\", \"index\": 0, \"prev_hash\": \"0\", \"timestamp\": 1750000581506, \"transactions\": []}"
    }
}
```

### Create Transaction
###### mutation | submitTransaction
```graphql
mutation {
    submitTransaction(sender: "Zilong", recipient: "Gusion", amount: 100) {
        ok
        message
    }
}
```
###### response
```json
{
    "data": {
        "submitTransaction": {
            "ok": true,
            "message": "Transaction received"
        }
    }
}
```

### Block Mining
###### mutation | mineBlock
```graphql
mutation {
    mineBlock {
        ok
        block
    }
}
```
###### response
```json
{
    "data": {
        "mineBlock": {
            "ok": true,
            "block": "{\"hash\": \"e4cb8377b0d7ab94cd465f7888a9a81654d14cb76665a79d6fee8307ccc37605\", \"index\": 1, \"prev_hash\": \"e24d032c5906e35f8da2ff39ccde24df3d4b23ea9d609df7f65522e0a9cba946\", \"timestamp\": 1750011100619, \"transactions\": [\"{\\\"sender\\\":\\\"Zilong\\\",\\\"recipient\\\":\\\"Gusion\\\",\\\"amount\\\":100}\"]}"
        }
    }
}
```