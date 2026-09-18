from django.contrib import admin

from .models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount', 'category', 'date', 'user', 'created_at')
    list_filter = ('category', 'date', 'user')
    search_fields = ('description', 'user__username')
    ordering = ('-date',)
    date_hierarchy = 'date'
