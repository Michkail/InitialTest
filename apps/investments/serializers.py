from rest_framework import serializers
from .models import UserInvestment


class UserInvestmentSerializer(serializers.ModelSerializer):
    profit_loss = serializers.SerializerMethodField()
    profit_loss_percentage = serializers.SerializerMethodField()

    class Meta:
        model = UserInvestment
        fields = ['id', 'asset_name', 'amount_invested', 'current_value',
                  'profit_loss', 'profit_loss_percentage', 'purchase_date']

    def get_profit_loss(self, obj):
        return str(obj.current_value - obj.amount_invested)

    def get_profit_loss_percentage(self, obj):
        if obj.amount_invested == 0:
            return "0.00"
        
        percent = ((obj.current_value - obj.amount_invested) / obj.amount_invested) * 100

        return f"{percent:.2f}"

class CreateUserInvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInvestment
        fields = ['asset_name', 'amount_invested', 'purchase_date', 'current_value', 'is_active']

    def validate_amount_invested(self, value):
        if value < 1000:
            raise serializers.ValidationError("Minimum investment is $1000")
        
        return value

    def to_representation(self, instance):
        data = super().to_representation(instance)
        roi = instance.current_value - instance.amount_invested
        roi_percentage = (roi / instance.amount_invested) * 100 if instance.amount_invested else 0

        data['profit_loss'] = f"{roi:.2f}"
        data['profit_loss_percentage'] = f"{roi_percentage:.2f}"

        return data
