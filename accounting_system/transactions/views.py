from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm, TransactionForm
from .models import UserProfile, Transaction
from django.views.decorators.csrf import csrf_protect


def home(request):
    return render(request, 'transactions/home.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'transactions/registration.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('add_transaction')
        else:
            messages.error(request, 'Invalid login credentials')
    return render(request, 'transactions/login.html')

# @login_required
# def account(request):
#     user_profile = UserProfile.objects.get(user=request.user)
#     transactions = Transaction.objects.filter(user_profile=user_profile)
#     return render(request, 'transactions/account.html', {'user_profile': user_profile, 'transactions': transactions, 'transaction_form': TransactionForm()})


# @csrf_protect
# @login_required
# def add_transaction(request):
#     user_profile = UserProfile.objects.get(user=request.user)
#     if request.method == 'POST':
#         form = TransactionForm(request.POST)
#         if form.is_valid():
#             transaction = form.save(commit=False)
#             transaction.user_profile = user_profile
#             transaction.save()
#             return redirect('add_transaction')
#     else:
#         form = TransactionForm()
#     return render(request, 'transactions/add_transaction.html', {'form': form})

from django.shortcuts import render, redirect
from .forms import TransactionForm
from .models import UserProfile, Transaction
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

@csrf_protect
@login_required
def add_transaction(request):
    user_profile = UserProfile.objects.get(user=request.user)
    new_transaction = None  # Variable to store the newly created transaction

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user_profile = user_profile
            transaction.save()
            new_transaction = transaction  # Assign the newly created transaction to the variable
    else:
        form = TransactionForm()

    transactions = Transaction.objects.filter(user_profile=user_profile)

    return render(request, 'transactions/add_transaction.html', {
        'form': form,
        'new_transaction': new_transaction,
        'transactions': transactions,  # You can include other transactions for display as well
    })



@login_required
def generate_report(request):
    user_profile = request.user.userprofile 
    transactions = Transaction.objects.filter(user_profile=user_profile)

    year_wise_transactions = {}  # Dictionary to store transactions year-wise

    for transaction in transactions:
        year = transaction.date.year
        if year not in year_wise_transactions:
            year_wise_transactions[year] = []

        year_wise_transactions[year].append(transaction)

    years = set(transaction.date.year for transaction in transactions)
    months = set(transaction.date.month for transaction in transactions)

    return render(request, 'transactions/generate_report.html', {
        'user_profile': user_profile,
        'year_wise_transactions': year_wise_transactions,
        'years': years,
        'months': months,
    })

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')
