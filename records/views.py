from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Record, Payment, Pawnshop, Profile
from django.shortcuts import render, redirect
from django.utils import timezone
from .forms import PawnshopForm, RecordForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout


class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, "records/register.html", {"form": form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user, role="customer")
            login(request, user)
            return redirect("index")
        else:
            return render(request, "records/register.html", {"form": form})


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, "records/login.html", {"form": form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("index")
        return render(request, "records/login.html", {"form": form})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect("index")


class PawnshopListView(View):
    """Class-based view to list all pawnshops."""

    def get(self, request):
        """Get all pawnshops, with optional search filtering."""
        query = request.GET.get('q')
        if query:
            pawnshops = Pawnshop.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        else:
            pawnshops = Pawnshop.objects.all()
        context = {'pawnshops': pawnshops,'query': query}
        return render(request, 'records/pawnshop_list.html', context)


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
        query = request.GET.get('q')
        active_records = Record.objects.filter(pawnshop=pawnshop, active=True)
        if query:
            active_records = active_records.filter(
                Q(name__icontains=query) | Q(detail__icontains=query)
            )
        context = {
            'pawnshop': pawnshop,
            'records': active_records,
            'query': query
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


class CreateRecordView(View):
    """View to create a new record for a specific pawnshop."""

    def get(self, request, pawnshop_id):
        """Get form to create record."""
        pawnshop = get_object_or_404(Pawnshop, id=pawnshop_id)
        initial_data = {
            'start_date': timezone.now(),
            'end_date': timezone.now() + timezone.timedelta(days=365),
        }
        form = RecordForm(initial=initial_data)
        return render(request, 'records/create_record.html', {'form': form, 'pawnshop': pawnshop})

    def post(self, request, pawnshop_id):
        """Handle post request to create record."""
        pawnshop = get_object_or_404(Pawnshop, id=pawnshop_id)
        form = RecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.pawnshop = pawnshop
            record.active = True
            record.save()
            messages.success(request, "Record created successfully!")
            return redirect('record_index', pawnshop_id = pawnshop.id)
        return render(request, 'records/create_record.html', {'form': form, 'pawnshop': pawnshop})
