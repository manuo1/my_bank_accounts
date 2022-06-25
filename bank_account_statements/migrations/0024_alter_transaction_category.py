# Generated by Django 4.0.4 on 2022-05-20 21:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('categorization', '0010_alter_categorykeyword_category_and_more'),
        ('bank_account_statements', '0023_transaction_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='category',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='categorization.category',
            ),
        ),
    ]
