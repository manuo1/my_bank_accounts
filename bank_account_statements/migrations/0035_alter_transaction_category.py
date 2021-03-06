# Generated by Django 4.0.4 on 2022-05-20 21:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('categorization', '0010_alter_categorykeyword_category_and_more'),
        ('bank_account_statements', '0034_alter_transaction_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='category',
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_DEFAULT,
                to='categorization.category',
            ),
        ),
    ]
