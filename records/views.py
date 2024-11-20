from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Record, Payment, Pawnshop, Profile, LoanOffer, Payment, Resell
from django.shortcuts import render, redirect
from django.utils import timezone
from .forms import PawnshopForm, RecordForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from datetime import datetime, date, timedelta


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
        active_records = Record.objects.filter(pawnshop=pawnshop)
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
        overdue = record.is_overdue()
        staff = record.loan_staff()
        customer = record.customer()
        print(record.item_status)

        context = {
            'record': record,
            'accrued_interest': accrued_interest,
            'total_due': total_due,
            'remaining_loan': remaining_loan,
            'payments': payments,
            'overdue': overdue,
            'staff': staff,
            'customer': customer,
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
            record.item_status = 0
            record.active = True
            record.save()
            # Logged in staff is determined to be staff of this record.
            LoanOffer.objects.create(
                user=request.user,
                record=record,
                is_staff=True
            )

            # Create a LoanOffer for the selected customer.
            customer_profile = form.cleaned_data['customer']
            LoanOffer.objects.create(
                user=customer_profile.user,
                record=record,
                is_staff=False
            )
            messages.success(request, "Record created successfully!")
            return redirect('record_index', pawnshop_id = pawnshop.id)
        return render(request, 'records/create_record.html', {'form': form, 'pawnshop': pawnshop})


def retrieveItem(request, pawnshop_id, record_id):
    """Retrieve item from record."""
    record = get_object_or_404(Record, pk=record_id, pawnshop_id=pawnshop_id)
    print(record)
    record.item_status = 2
    record.active = False
    record.save()
    print(record.item_status)
    return redirect('record_detail', pawnshop_id=pawnshop_id, record_id=record_id)


def monthly_statistics(request, pawnshop_id):
    """View to display daily statistics for a specific month and pawnshop."""
    pawnshop = get_object_or_404(Pawnshop, pk=pawnshop_id)
    month_input = request.GET.get('month', datetime.now().strftime('%Y-%m'))
    try:
        selected_date = datetime.strptime(month_input, '%Y-%m')
    except ValueError:
        selected_date = datetime.now()
    selected_year = selected_date.year
    selected_month = selected_date.month
    first_day = date(selected_year, selected_month, 1)
    if selected_month == 12:
        last_day = date(selected_year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = date(selected_year, selected_month + 1, 1) - timedelta(days=1)
    first_day = timezone.make_aware(datetime.combine(first_day, datetime.min.time()))
    last_day = timezone.make_aware(datetime.combine(last_day, datetime.min.time()))
    records = Record.objects.filter(
        pawnshop=pawnshop,
        start_date__gte=first_day,
        start_date__lte=last_day
    )
    payments = Payment.objects.filter(
        record__pawnshop=pawnshop,
        timestamp__gte=first_day,
        timestamp__lte=last_day
    )
    resells = Resell.objects.filter(
        record__pawnshop=pawnshop,
        timestamp__gte=first_day,
        timestamp__lte=last_day
    )
    payment_data = []
    for payment in payments:
        day = timezone.localtime(payment.timestamp).date()
        payment_data.append({
            'day': day,
            'total': payment.money
        })
    resell_data = []
    for resell in resells:
        day = timezone.localtime(resell.timestamp).date()
        resell_data.append({
            'day': day,
            'total': resell.money
        })
    income = {}
    for entry in payment_data:
        day = entry['day']
        income[day] = income.get(day, 0) + entry['total']
    for entry in resell_data:
        day = entry['day']
        income[day] = income.get(day, 0) + entry['total']
    expense_data = []
    for record in records:
        day = timezone.localtime(record.start_date).date()
        expense_data.append({
            'day': day,
            'total': record.loan_amount
        })
    expenses = {entry['day']: entry['total'] for entry in expense_data}
    days = sorted(set(income.keys()).union(expenses.keys()))
    income_chart_data = [income.get(day, 0) for day in days]
    expense_chart_data = [expenses.get(day, 0) for day in days]
    days_display = [day.strftime('%d %B %Y') for day in days]
    selected_month_display = selected_date.strftime('%B %Y')

    context = {
        'pawnshop': pawnshop,
        'selected_month': selected_date.strftime('%Y-%m'),
        'days': days_display,
        'income_chart_data': income_chart_data,
        'expense_chart_data': expense_chart_data,
        'selected_month_display': selected_month_display,
    }
    print(context) # to be removed
    return render(request, 'records/monthly_statistics.html', context)

