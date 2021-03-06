# Generated by Django 4.0.4 on 2022-05-25 22:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('categorization', '0019_alter_categorykeyword_options'),
        (
            'bank_account_statements',
            '0040_alter_bank_options_alter_statement_options_and_more',
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='category',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='categorization.category',
            ),
        ),
    ]
