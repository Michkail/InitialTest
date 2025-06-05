from django.urls import path
from .views import InvestmentListCreateView, InvestmentSummaryView


urlpatterns = [
    path('', InvestmentListCreateView.as_view(), name='investment-list-create'),
    path('summary/', InvestmentSummaryView.as_view(), name='investment-summary')
]