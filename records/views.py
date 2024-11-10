from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Record, Payment, Pawnshop
from django.shortcuts import render, redirect
from .forms import PawnshopForm
from django.contrib import messages

class PawnshopListView(View):
    """Class-based view to list all pawnshops."""

    def get(self, request):
        """Get all pawnshops."""
        active_records = Pawnshop.objects.all()
        return render(request, 'records/pawnshop_list.html', {'pawnshops': active_records})


class CreatePawnshopView(View):
    """View to create a new pawnshop."""
    
    def get(self, request):
        """Get form data."""
        form = PawnshopForm()
        return render(request, 'records/create_pawnshop.html', {'form': form})
    
    def post(self, request):
        """Create pawnshop."""
        form = PawnshopForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Pawnshop created successfully!")
            return redirect('index')
        return render(request, 'records/create_pawnshop.html', {'form': form})


class RecordIndex(View):
    """View to display a list of active records for a specific pawnshop."""

    def get(self, request, pawnshop_id):
        """Get all records in this pawnshop."""
        pawnshop = get_object_or_404(Pawnshop, pk=pawnshop_id)
        active_records = Record.objects.filter(pawnshop=pawnshop, active=True)
        
        context = {
            'pawnshop': pawnshop,
            'records': active_records
        }
        return render(request, 'records/record_index.html', context)


class RecordDetail(View):
    """View to display details of a single record."""

    def get(self, request, pawnshop_id, record_id):
        """Get specific record."""
        record = get_object_or_404(Record, pk=record_id, pawnshop_id=pawnshop_id)
        accrued_interest = record.accrued_interest()
        total_due = record.total_due()
        remaining_loan = record.remaining_loan_amount()
        payments = Payment.objects.filter(record=record)

        context = {
            'record': record,
            'accrued_interest': accrued_interest,
            'total_due': total_due,
            'remaining_loan': remaining_loan,
            'payments': payments
        }
        return render(request, 'records/record_detail.html', context)
