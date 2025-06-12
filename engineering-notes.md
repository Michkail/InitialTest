# System Engineering Notes
## 1. Why Celery + Redis?
**Celery** for background jobs such yield payments, statement generation, and rate updates.

**Redis** is the broker for **Celery** and also used for *Channels* (WebSocker layer), reducing infra overhead.

###### apps/investment/tasks.py
```python
@shared_task
def process_yield_payments():
    ...
```

###### config/settings.py
```python
CELERY_BROKER_URL = "
```

###### docker-compose.django.yml
```yml
command: ["sh", "-c", "uv run celery -A config worker -l info"]
```


## 2. Why Django Channels?
WebSocket support is needed to push live update *(e.g., yield payout or portfolio change)* to the client.

###### apps/notifications/consumers.py
```python
async def receive_json(self, content, **kwargs):
    if content.get("command") == "portfolio":
        await self.send_portfolio_summary()
```

###### docker-compose.django.yml
```yml
command: ["sh", "-c", "uv run manage.py makemigrations && uv run manage.py migrate && uv run daphne -b 0.0.0.0 -p 8088 config.asgi:application"]
```

## 3. How Multi-Currency Works?
Currencies and exchange rates are stored in Currency model. Rates are pulled from **CoinGecko** and converted dynamically.

###### apps/integrations/exchange/providers.py
```python
class ExchangeRateService:
    def convert(self, amount, from_currency, to_currency):
        ...
```

###### apps/investments/models.py
```python
class Currency(models.Model):
    code = models.CharField(...)
```

## 4. Smart Contract Integration
Mock settlement logic is implemented for yield payout to simulate blockchain tx hash.

###### apps/integrations/contracts/settlement.py
```python
class SmartContractSettlementService:
    def send_yield_to_wallet(self):
        return {
            "tx_hash": "...",
            "status": "submitted"
        }
```

used in: 

###### apps/investments/services/yield_calculation_service.py
```python
tx_result = SmartContractSettlementService().send_yield_to_wallet()
```

## 5. Modular Architecture
The codebase is split into multiple Django apps by domain:

```bash
┌── apps/
│   ├──	analytics/
│   ├──	integrations/
│   ├──	investments/
│   ├──	notifications/
│   ├──	users/
│   ├──	wallets/
```
Each app handles only its concern: *e.g.,* **wallets/** for balance, **investment/** for portfolio, etc.

## 6. Why settings.AUTH_USER_MODEL?
Because we're using **CustomUser**, every *FK* to user must reference:

```python
from django.conf import settings

user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
```
Instead of importing User directly, which causes conflicts.

## 7. Why DecimalField?
For accurate monetary calculations.

```python
amount_invested = models.DecimalField(max_digits=20, decimal_places=2)
```
Avoids float rounding issues in financial applications.

## 8. REST vs GraphQL?
- REST is used for structured APIs: list, create, summary.
- GraphQL provides flexible query patterns for internal dashboards.

Both are authenticated via JWT.

## 9. GraphQL JWT Authentication
Configured in settings:


```python
AUTHENTICATION_BACKENDS = [
    "graphql_jwt.backends.JSONWebTokenBackend",
    "django.contrib.auth.backends.ModelBackend"
]
```
Enabled in schema:
###### config/schema.py
```python
class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    refresh_token = graphql_jwt.Refresh.Field()
```

## 10. Celery Worker vs Beat
- worker: runs background tasks
- beat: schedules recurring tasks

```yml
command: uv run celery -A config worker -l info
command: uv run celery -A config beat -l info --scheduler ...
```
## 11. Celery Monitoring
Can integrate Flower:

```yml
flower:
  image: mher/flower
  command: flower --broker=redis://redis:6379/1
```
## 12. PostgreSQL over SQLite
PostgreSQL supports:
- JSON field
- Indexing
- Read replicas
- Transaction concurrency

###### docker-compose.postgres.yml

```yml
db:
  image: postgres:14
```
## 13. Index Usage
Index used for fields often filtered or joined.

```python
class Meta:
    indexes = [models.Index(fields=["user", "currency"])]
```

## 14. Query Optimization
Used raw SQL for complex summary logic, routed to read replica:

###### apps/investments/views.py

```python
with connection.cursor() as cursor:
    cursor.execute("SELECT SUM(...) FROM ...")
```

## 15. What Refactored
- Move yield logic to independent module
- Improve fraud ML model
- Add tests for yield + exchange
- Split Celery queues

## 16. Production Deployment Plan
- Use gunicorn + uvicorn workers or Daphne
- PostgreSQL managed DB
- Redis with persistence
- Nginx as reverse proxy
- CI/CD via GitHub Actions
- Sentry + Flower monitoring


```yml
ports:
  - "8088:8000"
```