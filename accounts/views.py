from django.shortcuts import render, redirect, get_object_or_404
from .forms import AccountForm, TransferForm
from .models import Account, Transfer

def account_list(request):
    accounts = Account.objects.all()
    return render(request, 'accounts/account_list.html', {'accounts': accounts})

def account_create(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('account_list')
    else:
        form = AccountForm()
    return render(request, 'accounts/account_form.html', {'form': form})

def account_update(request, pk):
    account = get_object_or_404(Account, pk=pk)
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect('account_list')
    else:
        form = AccountForm(instance=account)
    return render(request, 'accounts/account_form.html', {'form': form})

def account_delete(request, pk):
    account = get_object_or_404(Account, pk=pk)
    if request.method == 'POST':
        account.delete()
        return redirect('account_list')
    return render(request, 'accounts/account_confirm_delete.html', {'account': account})

def transfer_view(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transfer_success')
    else:
        form = TransferForm()
    return render(request, 'accounts/transfer.html', {'form': form})

def transfer_success(request):
    return render(request, 'accounts/transfer_success.html')

def transfer_history(request):
    transfers = Transfer.objects.all()
    return render(request, 'accounts/transfer_history.html', {'transfers': transfers})
