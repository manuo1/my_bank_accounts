from django.db import models
from django.db.models.signals import post_save, post_delete
from bank_account_statements.mutators import populates_database_with_data_from_this_statement
from bank_account_statements.services import get_date_in_filename, formated_date
class Bank(models.Model):

    FRENCH = 'fr'
    ENGLISH = 'en'
    FILENAME_DATE_FORMAT_CHOICES = [
        (FRENCH, 'Jours / Mois'),
        (ENGLISH, 'Mois / Jours'),
    ]

    name = models.CharField(max_length=255)
    filename_date_format = models.CharField(
        max_length=2,
        choices=FILENAME_DATE_FORMAT_CHOICES,
        default=FRENCH,
    )

    def __str__(self) -> str:
        return self.name

class Statement(models.Model):

    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    file = models.FileField(upload_to='bank_statements', max_length=500)
    date = models.DateField(null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f"{formated_date(self.date)} - {self.bank.name}"

    def save(self, *args, **kwargs):
        self.date = get_date_in_filename(self.file.name, self.bank.filename_date_format)
        if not Statement.objects.filter(date=self.date, bank=self.bank).exists():
            super().save(*args, **kwargs)

def statement_post_save(sender, instance, created, *args, **kwargs):
    if created:
        populates_database_with_data_from_this_statement(instance)

post_save.connect(statement_post_save, sender=Statement)
