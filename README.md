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
│   ├── asgi.py
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── apps
│   ├── investments
│   │   ├── migrations
│   │   │   ├── __init__.py
│   │   │   ├── 0002_rename_currrent_value_userinvestment_current_value.py
│   │   │   ├── 0001_initial.py
│   │   ├── services.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── admin.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   ├── views.py
├── pyproject.toml
├── db.sqlite3
├── README.md
├── .gitignore
├── .python-version
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
