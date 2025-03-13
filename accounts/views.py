from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from .forms import AccountForm, TransferForm  # Assuming you have these forms created
from .models import Account, Transfer
from django.core.exceptions import ValidationError

def account_list(request):
    """List all accounts."""
    accounts = Account.objects.all()
    return render(request, 'accounts/account_list.html', {'accounts': accounts})


def account_create(request):
    """Create a new account."""
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            try:
                new_account = form.save(commit=False)  # Do not save yet
                new_account.ac_no = Account.generate_random_account_number()  # Set random account number
                new_account.save()  # Now save the account
                return redirect('account_list')  # Redirect to the account list after creation
            except IntegrityError:
                form.add_error(None, "An error occurred while creating the account. Please try again.")
    else:
        form = AccountForm()
    return render(request, 'accounts/account_form.html', {'form': form})

def account_update(request, pk):
    """Update an existing account."""
    account = get_object_or_404(Account, pk=pk)
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            try:
                form.save()
                return redirect('account_list')
            except IntegrityError:
                form.add_error(None, "An error occurred while updating the account. Please try again.")
    else:
        form = AccountForm(instance=account)
    return render(request, 'accounts/account_form.html', {'form': form})

def account_delete(request, pk):
    """Delete an existing account."""
    account = get_object_or_404(Account, pk=pk)
    
    account.delete()
    return redirect('account_list')
        

def transfer_view(request):
    """Handle money transfers between accounts."""
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            transfer = form.save(commit=False)  # Prevent immediate save
            
            try:
                transfer.save()  # Save the transfer record
                return redirect('transfer_success')  # Redirect to success page
            except ValidationError as ve:
                form.add_error(None, str(ve))  # Add validation error message to the form
            except IntegrityError:
                form.add_error(None, "An error occurred while processing the transfer. Please try again.")
        else:
            # If the form is not valid, errors will be displayed automatically
            pass
    else:
        form = TransferForm()
    
    return render(request, 'accounts/transfer.html', {'form': form})

def transfer_success(request):
    """Display a success message after a transfer."""
    return render(request, 'accounts/transfer_success.html')

def transfer_history(request):
    """Display the history of transfers."""
    transfers = Transfer.objects.all()
    return render(request, 'accounts/transfer_history.html', {'transfers': transfers})
