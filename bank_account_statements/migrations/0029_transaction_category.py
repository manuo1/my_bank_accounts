# Generated by Django 4.0.4 on 2022-05-20 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank_account_statements', '0028_remove_transaction_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='category',
            field=models.CharField(default=None, max_length=255),
            preserve_default=False,
        ),
    ]
