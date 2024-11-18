"""Database Model for pawnshop app."""
import math
from typing import Any
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import timedelta
from django.db.models import Sum
from django.core.validators import MaxValueValidator, MinValueValidator


def next_year():
    """Get the time of next year."""
    return timezone.now() + timedelta(days=365)


class Pawnshop(models.Model):
    """Pawnshop model to store records."""
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1024)

    def __str__(self):
        """String to represent the pawnshop."""
        return f"Pawnshop: {self.name}"


class Record(models.Model):
    """Pawnshop record model to store data."""

    name = models.CharField(max_length=255)
    detail = models.CharField(max_length=1024)
    pawnshop = models.ForeignKey(Pawnshop, on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(
        default=next_year)
    loan_amount = models.IntegerField(
        null=False, blank=False, validators=[MinValueValidator(0)])
    active = models.BooleanField(default=True)
    interest_rate = models.FloatField(
        default=5,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )
    item_status = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5)
        ]
    )
    # Status of items
    # 0 = Item is in Pawnshop
    # 1 = Waiting for retrieval
    # 2 = Retrieved (then close the record)
    # 3 = Waiting for reselling
    # 4 = Resold (then close the record)
    # 5 = Lost

    def __str__(self) -> Any:
        """Return Record Name Name as string representative.

        :return: record name
        """
        return self.name

    def is_active(self) -> bool:
        """Check if contract is ended or not.

        :return: True if contract is active.
        """
        return self.active
    
    def is_overdue(self) -> bool:
        """Check if contract is overdue or not.

        :return: True if contract is overdue.
        """
        if self.end_date <= timezone.now():
            if self.item_status == 0:
                self.item_status = 3
            return True

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
        months_elapsed = math.floor(
            (timezone.now() - self.start_date).days / 30)
        # add interest per month
        interest = self.interest_rate/100
        return int(self.loan_amount * interest * months_elapsed)

    def total_due(self) -> int:
        """Calculate the total amount due (loan amount + accrued interest).

        :return: Total amount due
        """
        return self.loan_amount + self.accrued_interest()

    def remaining_loan_amount(self) -> int:
        """Calculate the remaining loan amount after payments, and close the record if fully paid.

        :return: Remaining loan amount
        """
        total_payments = self.payment_set.aggregate(Sum('money'))[
            'money__sum'] or 0
        remaining_amount = self.total_due() - total_payments

        # Close the record if payment exceed or equal to requirement
        if remaining_amount <= 0:
            self.item_status = 1
            self.save()

        return max(remaining_amount, 0)

    def has_been_resold(self) -> bool:
        """Check if the record has been resold.

        :return: True if the record has a related resell entry.
        """
        return self.resell_set.exists()

    def total_resell_income(self) -> int:
        """Calculate total income from resell.

        :return: Total income generated from reselling.
        """
        return self.resell_set.aggregate(Sum('money'))['money__sum'] or 0


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
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        """Return payment information.

        :return: user's username and the money they've paid
        """
        return f"User {self.user.username} paid {self.money} for {self.record.name} record"
    

class Resell(models.Model):
    """Income from resell the item."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    money = models.IntegerField(null=False, blank=False)
    timestamp = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        """Override save to mark the associated record as inactive."""
        super().save(*args, **kwargs)
        # Deactivate the associated record after resell
        if self.record.is_active():
            self.record.active = False
            self.record.save()

    def __str__(self) -> str:
        """Return income information."""
        return (
            f"User {self.user.username} gained {self.money} from "
            f"{self.record.name} item after reselling the contract."
        )
