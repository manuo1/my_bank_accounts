# Generated by Django 4.0.4 on 2022-05-16 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank_account_statements', '0018_alter_bank_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='statement',
            name='modified_date',
        ),
        migrations.AlterField(
            model_name='bank',
            name='filename_date_format',
            field=models.CharField(choices=[('fr', 'Jour / Mois / Année'), ('en', 'Année / Mois / Jour')], default='fr', max_length=2),
        ),
        migrations.AlterField(
            model_name='bank',
            name='name',
            field=models.CharField(choices=[('Crédit Mutuel', 'Crédit Mutuel'), ('Crédit Agricole', 'Crédit Agricole')], default='Crédit Agricole', max_length=15, unique=True),
        ),
        migrations.AlterField(
            model_name='statement',
            name='date',
            field=models.DateField(),
        ),
    ]
