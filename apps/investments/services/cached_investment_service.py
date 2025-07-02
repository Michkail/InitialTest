from django.core.cache import cache
from .statement_service import InvestmentService


class CachedInvestmentService:
    def get_portfolio_value(self, user_id):
        local_key = f"portfolio:mem:{user_id}"
        redis_key = f"portfolio:redis:{user_id}"

        value = cache.get(local_key)
        if value:
            return value

        value = cache.get(redis_key)
        if value:
            cache.set(local_key, value, timeout=10)
            return value

        value = InvestmentService().calculate_portfolio_value_by_user_id(user_id)
        cache.set(redis_key, value, timeout=60)
        cache.set(local_key, value, timeout=10)
        return value

    def invalidate_user_cache(self, user_id):
        cache.delete_many([
            f"portfolio:mem:{user_id}",
            f"portfolio:redis:{user_id}",
        ])
