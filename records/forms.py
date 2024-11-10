from django import forms
from .models import Pawnshop, Record


class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['name', 'detail', 'start_date', 'end_date', 'loan_amount', 'interest_rate']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class PawnshopForm(forms.ModelForm):
    class Meta:
        model = Pawnshop
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        }
