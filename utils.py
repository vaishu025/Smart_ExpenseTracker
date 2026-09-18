"""Helper functions for date filtering, CSV export, and PDF report generation."""

import csv
from datetime import timedelta

from django.http import HttpResponse
from django.utils import timezone

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer


def filter_expenses_by_period(queryset, period):
    """Filter an Expense queryset by 'today', 'week', 'month', or 'all'."""
    today = timezone.localdate()

    if period == 'today':
        return queryset.filter(date=today)
    elif period == 'week':
        start_of_week = today - timedelta(days=today.weekday())
        return queryset.filter(date__gte=start_of_week, date__lte=today)
    elif period == 'month':
        return queryset.filter(date__year=today.year, date__month=today.month)
    return queryset


def export_expenses_csv(expenses, filename='expenses.csv'):
    """Return an HttpResponse containing the given expenses as a CSV file."""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    writer.writerow(['Description', 'Amount', 'Category', 'Date'])

    for expense in expenses:
        writer.writerow([expense.description, expense.amount, expense.category, expense.date])

    return response


def export_expenses_pdf(expenses, username, total, filename='expense_report.pdf'):
    """Return an HttpResponse containing the given expenses as a PDF report."""
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    doc = SimpleDocTemplate(
        response, pagesize=A4,
        topMargin=2 * cm, bottomMargin=2 * cm,
        leftMargin=2 * cm, rightMargin=2 * cm,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle', parent=styles['Title'], fontSize=20, spaceAfter=6,
        textColor=colors.HexColor('#0d6efd'),
    )
    subtitle_style = ParagraphStyle(
        'SubtitleStyle', parent=styles['Heading2'], fontSize=13, spaceAfter=4,
    )
    normal_style = styles['Normal']

    elements = []
    elements.append(Paragraph('SMART EXPENSE TRACKER', title_style))
    elements.append(Paragraph('Expense Report', subtitle_style))
    elements.append(Paragraph(f'Username: {username}', normal_style))
    elements.append(Paragraph(f'Generated on: {timezone.localdate().strftime("%d %b %Y")}', normal_style))
    elements.append(Spacer(1, 0.6 * cm))

    data = [['Description', 'Amount (₹)', 'Category', 'Date']]
    for expense in expenses:
        data.append([
            expense.description,
            f'{expense.amount:.2f}',
            expense.category,
            expense.date.strftime('%d-%m-%Y'),
        ])

    if len(data) == 1:
        data.append(['No expenses recorded', '-', '-', '-'])

    table = Table(data, colWidths=[7 * cm, 3 * cm, 3.5 * cm, 3 * cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0d6efd')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f2f2f2')]),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(table)

    elements.append(Spacer(1, 0.8 * cm))
    total_style = ParagraphStyle(
        'TotalStyle', parent=styles['Heading2'], fontSize=13,
        textColor=colors.HexColor('#0d6efd'),
    )
    elements.append(Paragraph(f'Total Expenses: ₹{total:.2f}', total_style))

    doc.build(elements)
    return response
