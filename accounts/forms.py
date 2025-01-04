from django import forms
from .models import Account, Transfer
from django.core.exceptions import ValidationError

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['ac_name', 'ac_no', 'ac_mobile', 'email', 'account_type', 'balance']
        widgets={
            'ac_name':forms.TextInput(attrs={'class':'form-control'}),
            'ac_no':forms.TextInput(attrs={'class':'form-control'}),
            'ac_mobile':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'account_type':forms.Select(attrs={'class':'form-select','placeholder':'select account type'}),
            'balance':forms.NumberInput(attrs={'class':'form-control'}),
            
        }

class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = ['from_account', 'to_account', 'amount']
        widgets={
            'from_account': forms.Select(attrs={
                'class': 'form-select',  # Bootstrap class for dropdowns
                'placeholder': 'Select From Account',
            }),
            'to_account': forms.Select(attrs={
                'class': 'form-select',  # Bootstrap class for dropdowns
                'placeholder': 'Select To Account',
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',  # Bootstrap class for input fields
                'placeholder': 'Enter Amount',
            }),
        }

    
