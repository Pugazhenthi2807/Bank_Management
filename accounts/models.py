from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
import random

class Account(models.Model):
    ACCOUNT_TYPE_CHOICES = [
        ('Saving', 'Saving'),
        ('Current', 'Current'),
        ('OV', 'Overdraft'),
    ]

    ac_name = models.CharField(max_length=100, unique=True)  # Added max_length
    ac_no = models.CharField(max_length=12, unique=True)  # Changed max_length to 12
    ac_mobile = models.CharField(max_length=10)
    email = models.EmailField()
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE_CHOICES)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.ac_name} - {self.ac_no}"
    
    

    @staticmethod
    def generate_random_account_number():
        """Generate a unique random 12-digit account number."""
        while True:
            random_number = str(random.randint(100000000000, 999999999999))  # Generate a 12-digit number
            if not Account.objects.filter(ac_no=random_number).exists():
                return random_number

    def save(self, *args, **kwargs):
        # Generate account number if it is not set (e.g., during creation)
        if not self.ac_no:
            self.ac_no = self.generate_random_account_number()
        super().save(*args, **kwargs)

class Transfer(models.Model):
    from_account = models.ForeignKey(Account, related_name='transactions_from', on_delete=models.CASCADE)
    to_account = models.ForeignKey(Account, related_name='transactions_to', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_from = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0)
    amount_to = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0)
    from_status = models.CharField(max_length=20, editable=False, default='Debited')
    to_status = models.CharField(max_length=20, editable=False, default='Credited')
    datetime = models.DateTimeField(default=timezone.now, editable=False)

    def save(self, *args, **kwargs):
        # Allow transfers only if amount is greater than zero
        if self.amount <= 0:
            raise ValidationError("Transfer amount must be greater than zero.")

        # Check for transfers to the same account
        if self.from_account == self.to_account:
            raise ValidationError("Cannot transfer to the same account with a non-zero amount.")

        if self.from_account.balance < self.amount:
            raise ValidationError("Insufficient funds.")

        # Update balances before saving the transfer record
        self.from_account.balance -= self.amount
        self.to_account.balance += self.amount

        self.amount_from = self.amount
        self.amount_to = self.amount

        # Save accounts first to ensure balances are updated before saving transfer record
        self.from_account.save()
        self.to_account.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Transfer from {self.from_account} to {self.to_account} of {self.amount} on {self.datetime}"
