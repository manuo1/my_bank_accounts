# Generated by Django 4.0.4 on 2022-06-09 20:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('current_month', '0002_bankwebsitedata'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TransactionWithoutStatement',
        ),
    ]
