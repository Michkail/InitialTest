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
├── ├──	investments
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
###### Token Auth
```graphql
mutation {
	tokenAuth(username: "admin", password: "admin") {
		token
		refreshToken
	}
}
```
