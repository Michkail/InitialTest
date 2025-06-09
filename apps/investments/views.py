from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum, F
from django.db import transaction
from django.utils import timezone
from .models import UserInvestment, TransactionLog, TransactionChoices
from .serializers import UserInvestmentSerializer, CreateUserInvestmentSerializer
from .services import InvestmentService
import uuid


class InvestmentListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # return UserInvestment.objects.filter(user=self.request.user).order_by('-purchase_date')
        return (UserInvestment.objects.select_related('user', 'currency')
                .prefetch_related('yield_payments')
                .filter(user=self.request.user)
                .order_by('-purchase_date'))

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateUserInvestmentSerializer
        
        return UserInvestmentSerializer

    def perform_create(self, serializer):
        investment = serializer.save(user=self.request.user)
        TransactionLog.objects.create(user=self.request.user, 
                                      transaction_type=TransactionChoices.PURCHASE, 
                                      amount=investment.amount_invested,
                                      timestamp=timezone.now(), 
                                      reference_id=str(uuid.uuid4()))


class InvestmentSummaryView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        service = InvestmentService()

        performance = service.calculate_portfolio_performance(user)
        insights = service.get_investment_insights(user)

        investments = UserInvestment.objects.filter(user=user)
        total_invested = investments.aggregate(total=Sum('amount_invested'))['total'] or 0
        current_value = investments.aggregate(total=Sum('current_value'))['total'] or 0
        total_profit_loss = current_value - total_invested
        active_count = investments.filter(is_active=True).count()

        best = investments.order_by((F('current_value') - F('amount_invested')).desc()).first()
        worst = investments.order_by((F('current_value') - F('amount_invested')).asc()).first()

        return Response({
            "total_invested": str(total_invested),
            "current_value": str(current_value),
            "total_profit_loss": str(total_profit_loss),
            "active_investments": active_count,
            "best_performing": best.asset_name if best else None,
            "worst_performing": worst.asset_name if worst else None,
            "portfolio_roi_percentage": performance,
            "insights": insights
        })


class BulkInvestmentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        data = request.data

        if not isinstance(data, list):
            return Response({"detail": "Expected a list of objects."}, status=400)
        
        serializer = CreateUserInvestmentSerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        investments = serializer.save(user=request.user)

        return Response({"created": len(investments)}, status=status.HTTP_201_CREATED)
