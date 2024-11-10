from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Record, Payment
from django.http import HttpRequest
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404
from rest_framework import decorators, response


@decorators.api_view(['get'])
def csrf_token_view(request: HttpRequest) -> response.Response:  # pragma: no cover
    """Return csrf token."""
    csrf_token = get_token(request)
    return response.Response({'csrfToken': csrf_token})


class RecordIndex(View):
    """View to display a list of active records."""

    def get(self, request):
        # Fetch all active records
        active_records = Record.objects.filter(active=True)
        return render(request, 'records/record_index.html', {'records': active_records})


class RecordDetail(View):
    """View to display details of a single record."""

    def get(self, request, pk):
        # Get the specific record, or 404 if not found
        record = get_object_or_404(Record, pk=pk)
        
        # Calculate accrued interest, total due, and remaining loan amount
        accrued_interest = record.accrued_interest()
        total_due = record.total_due()
        remaining_loan = record.remaining_loan_amount()
        
        # Fetch all payments related to the record
        payments = Payment.objects.filter(record=record)

        context = {
            'record': record,
            'accrued_interest': accrued_interest,
            'total_due': total_due,
            'remaining_loan': remaining_loan,
            'payments': payments
        }
        return render(request, 'records/record_detail.html', context)
