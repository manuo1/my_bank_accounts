import re
import dateparser
from django.db import models
from django.forms import ValidationError
from django.http import HttpResponseRedirect

def get_date_in_filename(filename, date_formats):
    raw_date = re.findall("\d{1,4}[-/_]\d{1,4}[-/_]\d{1,4}",filename)
    if raw_date and date_formats:
        return dateparser.parse(raw_date[0],languages=[date_formats])

def formated_date(date):
    if date:
        return date.strftime('%d/%m/%Y')
   

class Bank(models.Model):
    FRENCH = 'fr'
    ENGLISH = 'en'
    FILENAME_DATE_FORMAT_CHOICES = [
        (FRENCH, 'Jours Mois'),
        (ENGLISH, 'Mois Jours'),
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
    name = models.CharField(max_length=255, blank=True)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    file = models.FileField(upload_to='bank_statements', max_length=500, unique=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    content_inserted_into_database = models.DateField(null=True, blank=True)
    
    def __str__(self) -> str:
        return f"{self.name} - {self.file.name}"

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = get_date_in_filename(self.file.name, self.bank.filename_date_format)
        if not self.name:
            self.name = f"{self.bank.name} - {formated_date(self.date)}"
        super().save(*args, **kwargs)