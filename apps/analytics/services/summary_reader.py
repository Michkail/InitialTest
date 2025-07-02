from django.db import connections


def get_user_investment_summary(user_id):
    with connections['replica'].cursor() as cursor:
        cursor.execute("SELECT * FROM investment_summary WHERE user_id = %s", [user_id])
        
        return cursor.fetchone()
