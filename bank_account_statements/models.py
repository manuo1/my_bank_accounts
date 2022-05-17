from django.db import models
from django.db.models.signals import post_save, post_delete
from bank_account_statements.constants import (
    CREDIT_AGRICOLE,
    CREDIT_MUTUEL,
    DATEPARSER_ENGLISH_CODE,
    DATEPARSER_FRENCH_CODE,
)
from bank_account_statements.services import (
    CreditAgricolPdfStatement,
    CreditMutuelPdfStatement,
    get_date_in_filename,
    get_base_date_format,
)


class Bank(models.Model):

    FILENAME_DATE_FORMAT_CHOICES = [
        (DATEPARSER_FRENCH_CODE, "Jour / Mois / Année"),
        (DATEPARSER_ENGLISH_CODE, "Année / Mois / Jour"),
    ]
    BANK_NAME_CHOICES = [
        (CREDIT_MUTUEL, CREDIT_MUTUEL),
        (CREDIT_AGRICOLE, CREDIT_AGRICOLE),
    ]

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

    def __str__(self) -> str:
        return self.name


class Statement(models.Model):

    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    file = models.FileField(upload_to="bank_statements", max_length=500)
    date = models.DateField()
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{get_base_date_format(self.date)} - {self.bank.name}"

    def save(self, *args, **kwargs):
        self.date = get_date_in_filename(self.file.name, self.bank.filename_date_format)
        if not Statement.objects.filter(date=self.date, bank=self.bank).exists():
            super().save(*args, **kwargs)


def statement_post_save(sender, instance, created, *args, **kwargs):
    if created:
        instance_list = []
        pdf_statement = CreditMutuelPdfStatement()

        if instance.bank.name == CREDIT_AGRICOLE:
            pdf_statement = CreditAgricolPdfStatement()

        for transaction in pdf_statement.get_transactions(instance.file.path):
            instance_list.append(
                Transaction(
                    statement=instance,
                    date=transaction[0],
                    label=transaction[1],
                    value=transaction[2],
                )
            )
        Transaction.objects.bulk_create(instance_list)


post_save.connect(statement_post_save, sender=Statement)


class Transaction(models.Model):
    statement = models.ForeignKey(Statement, on_delete=models.CASCADE)
    date = models.DateField()
    label = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.statement} - {get_base_date_format(self.date)} | {self.label} | {self.value}"
