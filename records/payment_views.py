from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from .models import Record, Payment
from .payment_form import PaymentForm
import logging

logger = logging.getLogger(__name__)

class CreatePaymentView(View):
    """View to handle creating a payment for a specific record."""

    def get(self, request, pawnshop_id, record_id):
        record = get_object_or_404(Record, pk=record_id)
        form = PaymentForm(record=record)
        return render(request, 'records/create_payment.html', {'form': form, 'record': record})

    def post(self, request, pawnshop_id, record_id):
        record = get_object_or_404(Record, pk=record_id)
        form = PaymentForm(request.POST, record=record)

        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.record = record
            payment.save()

            return redirect('record_detail', pawnshop_id=pawnshop_id, record_id=record.id)

        return render(request, 'records/create_payment.html', {'form': form, 'record': record})
