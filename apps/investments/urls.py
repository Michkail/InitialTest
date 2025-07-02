from django.urls import path
from .views import InvestmentListCreateView, InvestmentSummaryView, BulkInvestmentCreateView


urlpatterns = [
    path('', InvestmentListCreateView.as_view(), name='investment-list-create'),
    path('summary/', InvestmentSummaryView.as_view(), name='investment-summary'),
    path('bulk-create/', BulkInvestmentCreateView.as_view(), name='investment-bulk-create')
]