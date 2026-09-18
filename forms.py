from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Expense


class RegisterForm(UserCreationForm):
    """Registration form that extends Django's built-in user creation form
    with an email field."""

    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with this email already exists.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class ExpenseForm(forms.ModelForm):
    """Form used for both adding and editing an expense."""

    class Meta:
        model = Expense
        fields = ['description', 'amount', 'category', 'date']
        widgets = {
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Uber to college, Pizza and burger, Electricity bill...',
                'id': 'id_description',
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter amount',
                'step': '0.01',
                'min': '0.01',
            }),
            'category': forms.Select(attrs={'class': 'form-select', 'id': 'id_category'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean_description(self):
        description = self.cleaned_data.get('description', '').strip()
        if not description:
            raise forms.ValidationError('Description cannot be empty.')
        return description

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is None:
            raise forms.ValidationError('Amount is required.')
        if amount <= 0:
            raise forms.ValidationError('Amount must be greater than zero.')
        return amount
