# Generated by Django 4.0.4 on 2022-05-22 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank_account_statements', '0037_transaction_category_transaction_extended_label'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='extended_label',
            field=models.CharField(max_length=255),
        ),
    ]
