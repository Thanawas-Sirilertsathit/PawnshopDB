from django import forms
from .models import Pawnshop

class PawnshopForm(forms.ModelForm):
    class Meta:
        model = Pawnshop
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        }
