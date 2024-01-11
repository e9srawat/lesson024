# transactions/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Transaction,User

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['category', 'mode_of_payment', 'amount', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
