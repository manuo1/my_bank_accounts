# Generated by Django 4.0.4 on 2022-05-14 21:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bank_account_statements', '0008_alter_statement_file'),
    ]

    operations = [
        migrations.RenameField(
            model_name='statement',
            old_name='date_modified',
            new_name='modified_date',
        ),
    ]