# Generated by Django 4.0.4 on 2022-05-19 19:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bank_account_statements', '0021_remove_statement_category_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='category',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='periodicity',
        ),
    ]