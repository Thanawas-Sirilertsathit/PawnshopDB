from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Pawnshop, Record, LoanOffer, Payment

class PawnshopSerializer(serializers.ModelSerializer):
    """Serializer for the Pawnshop model."""
    
    class Meta:
        model = Pawnshop
        fields = ['id', 'name', 'description']


class RecordSerializer(serializers.ModelSerializer):
    """Serializer for the Record model."""
    accrued_interest = serializers.ReadOnlyField()
    total_due = serializers.ReadOnlyField()
    remaining_loan_amount = serializers.ReadOnlyField()
    loan_staff = serializers.SerializerMethodField()
    customer = serializers.SerializerMethodField()
    pawnshop = PawnshopSerializer(read_only=True)

    class Meta:
        model = Record
        fields = [
            'id', 'name', 'detail', 'pawnshop', 'start_date', 'end_date',
            'loan_amount', 'active', 'interest_rate', 'accrued_interest',
            'total_due', 'remaining_loan_amount', 'loan_staff', 'customer'
        ]

    def get_loan_staff(self, obj):
        """Get the user who is the staff member for the loan."""
        staff = obj.loan_staff()
        return staff.username if staff else None

    def get_customer(self, obj):
        """Get the customer user for the loan."""
        customer = obj.customer()
        return customer.username if customer else None


class LoanOfferSerializer(serializers.ModelSerializer):
    """Serializer for the LoanOffer model."""
    user = serializers.StringRelatedField()
    record = serializers.StringRelatedField()

    class Meta:
        model = LoanOffer
        fields = ['id', 'user', 'record', 'is_staff']


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for the Payment model."""
    user = serializers.StringRelatedField()
    record = serializers.StringRelatedField()

    class Meta:
        model = Payment
        fields = ['id', 'user', 'record', 'money']
