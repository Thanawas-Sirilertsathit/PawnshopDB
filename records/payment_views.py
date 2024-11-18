from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from .models import Record, Payment
from django.contrib import messages
from .payment_form import PaymentForm, ResellForm
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


class CreateResellView(View):
    """View to handle creating a resell transaction for a specific record."""

    def get(self, request, pawnshop_id, record_id):
        record = get_object_or_404(Record, pk=record_id)
        
        # Prevent resell for closed records
        if not record.active:
            messages.error(request, "Cannot resell a closed record.")
            return redirect('record_detail', pawnshop_id=pawnshop_id, record_id=record.id)

        if not record.is_overdue():
            messages.error(request, "Cannot resell non-overdue record.")
            return redirect('record_detail', pawnshop_id=pawnshop_id, record_id=record.id)

        form = ResellForm()
        return render(request, 'records/create_resell.html', {'form': form, 'record': record})

    def post(self, request, pawnshop_id, record_id):
        record = get_object_or_404(Record, pk=record_id)
        
        if not record.active:
            messages.error(request, "Cannot resell a closed record.")
            return redirect('record_detail', pawnshop_id=pawnshop_id, record_id=record.id)

        if not record.is_overdue():
            messages.error(request, "Cannot resell non-overdue record.")
            return redirect('record_detail', pawnshop_id=pawnshop_id, record_id=record.id)

        form = ResellForm(request.POST)
        if form.is_valid():
            resell = form.save(commit=False)
            resell.user = request.user
            resell.record = record
            resell.save()

            record.active = False
            record.item_status = 4
            record.save()

            messages.success(request, "Resell transaction created successfully.")
            return redirect('record_detail', pawnshop_id=pawnshop_id, record_id=record.id)

        return render(request, 'records/create_resell.html', {'form': form, 'record': record})
