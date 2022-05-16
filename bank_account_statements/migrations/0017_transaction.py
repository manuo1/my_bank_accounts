# Generated by Django 4.0.4 on 2022-05-16 18:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bank_account_statements', '0016_remove_statement_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('label', models.CharField(max_length=255)),
                ('value', models.DecimalField(decimal_places=2, max_digits=20)),
                ('statement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bank_account_statements.statement')),
            ],
        ),
    ]
