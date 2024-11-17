from django import forms
from .models import Payment, Record

class PaymentForm(forms.ModelForm):
    """Form for creating a payment."""

    class Meta:
        model = Payment
        fields = ['money']

    def __init__(self, *args, **kwargs):
        self.record = kwargs.pop('record', None)
        super().__init__(*args, **kwargs)

    def clean_money(self):
        money = self.cleaned_data['money']

        if self.record is None:
            raise forms.ValidationError("Record is not selected.")

        if not self.record.is_active():
            raise forms.ValidationError("This record is closed.")

        remaining_amount = self.record.remaining_loan_amount()
        if money > remaining_amount:
            raise forms.ValidationError(
                f"Payment exceeds the remaining loan amount ({remaining_amount})."
            )

        return money
