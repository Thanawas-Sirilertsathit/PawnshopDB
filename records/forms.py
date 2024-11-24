from django import forms
from .models import Pawnshop, Record, Profile
from django.core.exceptions import ValidationError


class RecordForm(forms.ModelForm):
    customer = forms.ModelChoiceField(
        queryset=Profile.objects.filter(
            role="customer").select_related('user'),
        required=True,
        label="Select Customer",
        widget=forms.Select(attrs={
            'class': 'input input-bordered bg-neutral w-[80vh] rounded-xl-important text-primary border-2 border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary',
        })
    )

    class Meta:
        model = Record
        fields = ['name', 'detail', 'start_date', 'end_date',
                  'loan_amount', 'interest_rate', 'customer', 'active', 'item_status']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        """Validate data."""
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date and end_date < start_date:
            raise ValidationError(
                "End date cannot be earlier than start date.")

        return cleaned_data


class PawnshopForm(forms.ModelForm):
    class Meta:
        model = Pawnshop
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        }
