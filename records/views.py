from django.views import View
from .models import Record, Pawnshop, Profile, LoanOffer, Payment, Resell
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .forms import PawnshopForm, RecordForm, EditRecordForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from functools import wraps
from datetime import datetime, date, timedelta
from collections import defaultdict


def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            try:
                user_profile = Profile.objects.get(user=request.user)
                if user_profile.role != role:
                    messages.warning(request, f"You do not have the permissions of {role} "
                                              f"as you are the {user_profile.role}.")
                    return redirect(request.META.get('HTTP_REFERER', 'index'))
            except Profile.DoesNotExist:
                messages.error(
                    request, "Profile not found. Please contact support.")
                return redirect(request.META.get('HTTP_REFERER', 'index'))
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


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
            pawnshops = Pawnshop.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query))
        else:
            pawnshops = Pawnshop.objects.all()
        context = {'pawnshops': pawnshops, 'query': query}
        context = {'pawnshops': pawnshops, 'query': query}
        return render(request, 'records/pawnshop_list.html', context)


@method_decorator([login_required, role_required("staff")], name="dispatch")
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
        record = get_object_or_404(
            Record, pk=record_id, pawnshop_id=pawnshop_id)
        accrued_interest = record.accrued_interest()
        total_due = record.total_due()
        remaining_loan = record.remaining_loan_amount()
        payments = Payment.objects.filter(record=record)
        overdue = record.is_overdue()

        # Handle loan_staff gracefully
        staff = record.loan_staff()
        staff_user = staff if staff else "No staff assigned"

        customer = record.customer()

        context = {
            'record': record,
            'accrued_interest': accrued_interest,
            'total_due': total_due,
            'remaining_loan': remaining_loan,
            'payments': payments,
            'overdue': overdue,
            'staff': staff_user,  # Use the variable that accounts for None
            'customer': customer,
        }
        return render(request, 'records/record_detail.html', context)


@method_decorator([login_required, role_required("staff")], name="dispatch")
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
            return redirect('record_index', pawnshop_id=pawnshop.id)
        return render(request, 'records/create_record.html', {'form': form, 'pawnshop': pawnshop})


def retrieveItem(request, pawnshop_id, record_id):
    """Retrieve item from record."""
    record = get_object_or_404(Record, pk=record_id, pawnshop_id=pawnshop_id)
    try:
        user_profile = Profile.objects.get(user=request.user)
        if user_profile.role != 'customer' or record.customer() != request.user:
            messages.warning(
                request, "You are not the customer of this record.")
            return redirect(request.META.get('HTTP_REFERER', 'index'))
    except Profile.DoesNotExist:
        messages.error(request, "Profile not found. Please contact support.")
        return redirect(request.META.get('HTTP_REFERER', 'index'))
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
        last_day = date(selected_year, selected_month +
                        1, 1) - timedelta(days=1)
    first_day = timezone.make_aware(
        datetime.combine(first_day, datetime.min.time()))
    last_day = timezone.make_aware(
        datetime.combine(last_day, datetime.min.time()))
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
    return render(request, 'records/monthly_statistics.html', context)


@method_decorator([login_required, role_required("staff")], name="dispatch")
class EditRecordView(View):
    """View to edit an existing record for a specific pawnshop."""

    def get(self, request, pawnshop_id, record_id):
        record = get_object_or_404(Record, pk=record_id)
        if record.loan_staff() != request.user:
            messages.warning(request, f"You are not the staff of this record.")
            return redirect(request.META.get('HTTP_REFERER', 'index'))

        form = EditRecordForm(instance=record, initial={
                              'customer': record.customer(), 'staff': record.loan_staff()})
        return render(request, 'records/edit_record.html', {'form': form, 'record': record})

    def post(self, request, pawnshop_id, record_id):
        record = get_object_or_404(Record, pk=record_id)
        if record.loan_staff() != request.user:
            messages.warning(request, f"You are not the staff of this record.")
            return redirect(request.META.get('HTTP_REFERER', 'index'))

        form = EditRecordForm(request.POST, instance=record)
        if form.is_valid():
            update_record = form.save(commit=False)
            update_record.user = request.user
            update_record.record = record
            update_record.save()
            # Get the selected staff from the form
            staff = form.cleaned_data['staff']
            LoanOffer.objects.update_or_create(
                record=update_record,
                is_staff=True,
                # Update or create with this user
                defaults={'user': staff.user}
            )

            messages.success(request, "Record update successfully.")
            return redirect('record_detail', pawnshop_id=pawnshop_id, record_id=record.id)
        return render(request, 'records/edit_record.html', {'form': form, 'record': record})


def yearly_report(request, pawnshop_id):
    """View to display yearly statistics for loans and repayments."""
    year_input = request.GET.get('year', datetime.now().year)
    try:
        selected_year = int(year_input)
    except ValueError:
        selected_year = datetime.now().year

    customer = get_object_or_404(Profile, user=request.user)

    first_day = timezone.make_aware(datetime(selected_year, 1, 1))
    last_day = timezone.make_aware(datetime(selected_year, 12, 31, 23, 59, 59))
    pawnshop = get_object_or_404(Pawnshop, pk=pawnshop_id)

    loans = Record.objects.filter(
        loanoffer__user=customer.user,
        loanoffer__is_staff=False,
        start_date__gte=first_day,
        start_date__lte=last_day,
        pawnshop=pawnshop
    )

    repayments = Payment.objects.filter(
        record__loanoffer__user=customer.user,
        record__loanoffer__is_staff=False,
        record__pawnshop=pawnshop,
        timestamp__gte=first_day,
        timestamp__lte=last_day
    )

    loans_by_month = defaultdict(int)
    for loan in loans:
        month = loan.start_date.strftime('%Y-%m')
        loans_by_month[month] += loan.loan_amount

    repayments_by_month = defaultdict(int)
    for repayment in repayments:
        month = repayment.timestamp.strftime('%Y-%m')
        repayments_by_month[month] += repayment.money
    months = [datetime(selected_year, i, 1).strftime('%Y-%m')
              for i in range(1, 13)]
    loan_chart_data = [loans_by_month.get(month, 0) for month in months]
    repayment_chart_data = [
        repayments_by_month.get(month, 0) for month in months]
    months_display = [datetime.strptime(
        month, '%Y-%m').strftime('%B') for month in months]
    selected_year_display = str(selected_year)

    context = {
        'customer': customer,
        'selected_year': selected_year,
        'months': months_display,
        'loan_chart_data': loan_chart_data,
        'repayment_chart_data': repayment_chart_data,
        'selected_year_display': selected_year_display,
        'pawnshop': pawnshop,
    }

    return render(request, 'records/yearly_report.html', context)
