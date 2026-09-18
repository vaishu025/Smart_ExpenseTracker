from datetime import timedelta

import plotly.graph_objects as go
from plotly.offline import plot as plotly_plot

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .category_predictor import predict_category
from .forms import RegisterForm, ExpenseForm
from .models import Expense
from .utils import filter_expenses_by_period, export_expenses_csv, export_expenses_pdf


def register_view(request):
    """Handle new user registration."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}! Your account has been created.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})


@login_required
def dashboard_view(request):
    """Main dashboard showing summary cards, filters, and recent expenses."""
    user_expenses = Expense.objects.filter(user=request.user)
    today = timezone.localdate()
    start_of_week = today - timedelta(days=today.weekday())

    total_expenses = user_expenses.aggregate(total=Sum('amount'))['total'] or 0
    today_expenses = user_expenses.filter(date=today).aggregate(total=Sum('amount'))['total'] or 0
    week_expenses = user_expenses.filter(date__gte=start_of_week, date__lte=today).aggregate(
        total=Sum('amount'))['total'] or 0
    month_expenses = user_expenses.filter(date__year=today.year, date__month=today.month).aggregate(
        total=Sum('amount'))['total'] or 0

    period = request.GET.get('period', 'all')
    filtered_expenses = filter_expenses_by_period(user_expenses, period)
    filtered_total = filtered_expenses.aggregate(total=Sum('amount'))['total'] or 0

    context = {
        'total_expenses': total_expenses,
        'today_expenses': today_expenses,
        'week_expenses': week_expenses,
        'month_expenses': month_expenses,
        'expenses': filtered_expenses,
        'filtered_total': filtered_total,
        'active_period': period,
        'expense_count': user_expenses.count(),
    }
    return render(request, 'expenses/dashboard.html', context)


@login_required
def add_expense_view(request):
    """Add a new expense, predicting the category from the description."""
    predicted_category = ''

    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, 'Expense added successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        description = request.GET.get('description', '')
        initial = {'date': timezone.localdate()}
        if description:
            initial['description'] = description
            predicted_category = predict_category(description)
            initial['category'] = predicted_category
        form = ExpenseForm(initial=initial)

    return render(request, 'expenses/add_expense.html', {
        'form': form,
        'predicted_category': predicted_category,
    })


@login_required
def predict_category_ajax(request):
    """Simple endpoint used by JS to live-predict a category as the user types."""
    description = request.GET.get('description', '')
    category = predict_category(description)
    return JsonResponse({'category': category})


@login_required
def edit_expense_view(request, pk):
    """Edit an existing expense. Only the owner may edit it."""
    expense = get_object_or_404(Expense, pk=pk, user=request.user)

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense updated successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ExpenseForm(instance=expense)

    return render(request, 'expenses/edit_expense.html', {'form': form, 'expense': expense})


@login_required
def delete_expense_view(request, pk):
    """Delete an existing expense after confirmation. Only the owner may delete it."""
    expense = get_object_or_404(Expense, pk=pk, user=request.user)

    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Expense deleted successfully!')
        return redirect('dashboard')

    return render(request, 'expenses/confirm_delete.html', {'expense': expense})


@login_required
def analytics_view(request):
    """Show Plotly visualizations for the logged-in user's expenses only."""
    user_expenses = Expense.objects.filter(user=request.user)

    category_totals = (
        user_expenses.values('category')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )

    pie_html = None
    line_html = None

    if category_totals:
        labels = [row['category'] for row in category_totals]
        values = [float(row['total']) for row in category_totals]

        pie_fig = go.Figure(data=[go.Pie(
            labels=labels, values=values, hole=0.45,
            marker=dict(colors=[
                '#0d6efd', '#6610f2', '#d63384', '#dc3545',
                '#fd7e14', '#ffc107', '#198754', '#20c997',
            ]),
        )])
        pie_fig.update_layout(
            title='Category-wise Expense Distribution',
            margin=dict(t=60, b=20, l=20, r=20),
            legend=dict(orientation='h', yanchor='bottom', y=-0.2),
        )
        pie_html = plotly_plot(pie_fig, output_type='div', include_plotlyjs='cdn')

    date_totals = (
        user_expenses.values('date')
        .annotate(total=Sum('amount'))
        .order_by('date')
    )

    if date_totals:
        dates = [row['date'] for row in date_totals]
        totals = [float(row['total']) for row in date_totals]

        line_fig = go.Figure(data=[go.Scatter(
            x=dates, y=totals, mode='lines+markers',
            line=dict(color='#0d6efd', width=3),
            marker=dict(size=7),
        )])
        line_fig.update_layout(
            title='Total Expenses Over Time',
            xaxis_title='Date',
            yaxis_title='Amount (₹)',
            margin=dict(t=60, b=40, l=50, r=20),
        )
        line_html = plotly_plot(line_fig, output_type='div', include_plotlyjs=False)

    return render(request, 'expenses/analytics.html', {
        'pie_html': pie_html,
        'line_html': line_html,
        'has_data': bool(category_totals),
    })


@login_required
def download_csv_view(request):
    """Download the logged-in user's expenses as a CSV file."""
    expenses = Expense.objects.filter(user=request.user)
    return export_expenses_csv(expenses, filename=f'{request.user.username}_expenses.csv')


@login_required
def download_pdf_view(request):
    """Download the logged-in user's expenses as a PDF report."""
    expenses = Expense.objects.filter(user=request.user)
    total = expenses.aggregate(total=Sum('amount'))['total'] or 0
    return export_expenses_pdf(
        expenses, request.user.username, total,
        filename=f'{request.user.username}_expense_report.pdf',
    )
