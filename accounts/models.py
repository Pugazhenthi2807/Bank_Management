from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


class Account(models.Model):
    ACCOUNT_TYPE_CHOICES = [
        ('Saving', 'Saving'),
        ('Current', 'Current'),
        ('OV', 'Overdraft'),
    ]

    ac_name = models.CharField(max_length=100)
    ac_no = models.CharField(max_length=20, unique=True)
    ac_mobile = models.CharField(max_length=15)
    email = models.EmailField()
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE_CHOICES)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.ac_name} - {self.ac_no}"


class Transfer(models.Model):
    from_account = models.ForeignKey(Account, related_name='transactions_from', on_delete=models.CASCADE)
    to_account = models.ForeignKey(Account, related_name='transactions_to', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_from = models.IntegerField(editable=False, default=0)
    amount_to = models.IntegerField(editable=False, default=0)
    from_status = models.CharField(max_length=20, editable=False, default='debited')
    to_status = models.CharField(max_length=20, editable=False, default='credited')
    datetime = models.DateTimeField(default=timezone.now, editable=False)

    # datetime = models.DateTimeField(default=timezone.now)


    def save(self, *args, **kwargs):
        # if self.from_account == self.to_account:
        #     raise ValidationError("Cannot transfer to the same account.")
        #
        # if self.from_account.balance < self.amount:
        #     raise ValidationError("Insufficient funds.")

        if self.from_account.balance >= self.amount:
            self.from_account.balance -= self.amount
            self.to_account.balance += self.amount

            self.amount_from = self.amount
            self.amount_to = self.amount

            self.from_status = 'Debited'
            self.to_status = 'Credited'

            self.from_account.save()
            self.to_account.save()

            super().save(*args, **kwargs)

    def __str__(self):
        return f"Transfer from {self.from_account} to {self.to_account} of {self.amount} on {self.datetime}"
