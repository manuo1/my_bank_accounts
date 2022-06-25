# Generated by Django 4.0.4 on 2022-05-22 21:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bank_account_statements', '0036_remove_transaction_category'),
        ('categorization', '0013_alter_categorykeyword_keyword'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionData',
            fields=[
                (
                    'my_data',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to='bank_account_statements.transaction',
                    ),
                ),
            ],
        ),
    ]
