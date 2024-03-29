
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add other user-related fields if needed

    def __str__(self):
        return self.user.username

class Transaction(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=[('food', 'Food'), ('travel', 'Travel'), ('entertainment', 'Entertainment'), ('rent', 'Rent')])
    mode_of_payment = models.CharField(max_length=50, choices=[('debit', 'Debit'), ('credit', 'Credit')])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.date} - {self.category} - {self.amount} - {self.mode_of_payment}"
