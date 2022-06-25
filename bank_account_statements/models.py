from django.db import models
from django.db.models.signals import post_save
from bank_account_statements.constants import (
    BANK_NAME_CHOICES,
    CREDIT_AGRICOLE,
    DATEPARSER_FRENCH_CODE,
    FILENAME_DATE_FORMAT_CHOICES,
)
from bank_account_statements.mutators import create_transaction_with_statement
from bank_account_statements.services import (
    get_date_in_filename,
    common_date_format,
    transaction_extended_label,
)
from categorization.models import Category
from categorization.mutators import update_transactions_category


class Bank(models.Model):

    name = models.CharField(
        unique=True,
        max_length=15,
        choices=BANK_NAME_CHOICES,
        default=CREDIT_AGRICOLE,
    )
    filename_date_format = models.CharField(
        max_length=2,
        choices=FILENAME_DATE_FORMAT_CHOICES,
        default=DATEPARSER_FRENCH_CODE,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Statement(models.Model):

    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    file = models.FileField(upload_to="bank_statements", max_length=500)
    date = models.DateField()
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "bank"]

    def __str__(self) -> str:
        return f"{common_date_format(self.date)} - {self.bank.name}"

    def save(self, *args, **kwargs):
        self.date = get_date_in_filename(
            self.file.name, self.bank.filename_date_format
        )
        if not Statement.objects.filter(
            date=self.date, bank=self.bank
        ).exists():
            super().save(*args, **kwargs)


def statement_post_save(sender, instance, created, *args, **kwargs):
    if created:
        create_transaction_with_statement(instance)
        update_transactions_category()


post_save.connect(statement_post_save, sender=Statement)


class Transaction(models.Model):
    statement = models.ForeignKey(
        Statement, null=True, blank=True, on_delete=models.CASCADE
    )
    date = models.DateField()
    label = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=20, decimal_places=2)
    category = models.ForeignKey(
        Category, blank=True, null=True, on_delete=models.SET_NULL
    )
    extended_label = models.CharField(max_length=255, blank=True)
    custom_label = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["-date", "label"]

    def __str__(self) -> str:
        return f"{self.statement} - {common_date_format(self.date)} | {self.label} | {self.value}"

    def save(self, *args, **kwargs):
        bank_name = ""
        if self.statement:
            bank_name = self.statement.bank.name
        self.extended_label = transaction_extended_label(
            label=self.label,
            custom_label=self.custom_label,
            value=self.value,
            date=self.date,
            statement_bank_name=bank_name,
        )
        super().save(*args, **kwargs)
        update_transactions_category()
