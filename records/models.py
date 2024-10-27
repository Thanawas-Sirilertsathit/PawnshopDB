"""Database Model for activities app."""
import math
from typing import Any
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import timedelta
from django.db.models import Sum


class Record(models.Model):
    """Pawnshop record model to store data."""

    name = models.CharField(max_length=255)
    detail = models.CharField(max_length=1024)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now() + timedelta(days=365))
    loan_amount = models.IntegerField(null=False, blank=False)
    active = models.BooleanField(default=True)
    interest_rate = models.FloatField(default=0.05)

    def __str__(self) -> Any:
        """Return Record Name Name as string representative.

        :return: record name
        """
        return self.name

    def is_active(self) -> Any:
        """Check if contract is ended or not.

        :return: True if contract is active.
        """
        return self.end_date >= timezone.now() and self.active


    def loan_staff(self) -> User:
        """Find user that is host of the loan (is_staff is True).

        :return: the staff who lends the loan of this contract
        """
        return LoanOffer.objects.filter(record=self, is_staff=True).first().user

    def customer(self) -> list[User]:
        """Find a customer user of the activity (host excluded).

        :return: customer of this loan contract
        """
        return LoanOffer.objects.filter(record=self, is_staff=False).first().user

    def accrued_interest(self) -> int:
        """Calculate the interest accrued based on 5% monthly interest.

        :return: Total accrued interest
        """
        # Calculate the number of full months since the loan start
        months_elapsed = math.floor((timezone.now() - self.start_date).days / 30)
        # 5% interest per month
        return int(self.loan_amount * self.interest_rate * months_elapsed)

    def total_due(self) -> int:
        """Calculate the total amount due (loan amount + accrued interest).

        :return: Total amount due
        """
        return self.loan_amount + self.accrued_interest()

    def remaining_loan_amount(self) -> int:
        """Calculate the remaining loan amount after payments, and close the record if fully paid.

        :return: Remaining loan amount
        """
        total_payments = self.payment_set.aggregate(Sum('money'))['money__sum'] or 0
        remaining_amount = self.total_due() - total_payments

        # Close the record if payment exceed or equal to requirement
        if remaining_amount <= 0:
            self.active = False
            self.save()

        return max(remaining_amount, 0) 


class LoanOffer(models.Model):
    """Loan model to store loan."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    is_staff = models.BooleanField(default=False)

    def __str__(self) -> str:
        """Return loan information.

        :return: user's username and the activity they've joined
        """
        return f"User {self.user.username} signed {self.record.name} record"


class Payment(models.Model):
    """Payment model to store transactions."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    money = models.IntegerField(null=False, blank=False)

    def __str__(self) -> str:
        """Return payment information.

        :return: user's username and the activity they've joined
        """
        return f"User {self.user.username} paid {self.money} for {self.record.name} record"
