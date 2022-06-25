# Generated by Django 4.0.4 on 2022-05-14 18:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='BankStatement',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('name', models.CharField(max_length=255)),
                ('file', models.FileField(upload_to='bank_statements/None')),
                (
                    'bank',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='bank_account_statements.bank',
                    ),
                ),
            ],
        ),
    ]
