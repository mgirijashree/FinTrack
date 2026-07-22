from django.db import models


class Category(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    gst_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=18.00
    )

    def __str__(self):
        return self.name


class Transaction(models.Model):

    TRANSACTION_TYPES = [
        ("Income", "Income"),
        ("Expense", "Expense"),
    ]

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    date = models.DateField()

    description = models.TextField()

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPES
    )

    def __str__(self):
        return f"{self.description} - ₹{self.amount}"


class Gst(models.Model):

    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE
    )

    gst_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    gst_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return f"{self.transaction.description} - {self.gst_percentage}%"

class Ledger(models.Model):

    date = models.DateField()

    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.CASCADE
    )

    current_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.date} - ₹{self.current_balance}"