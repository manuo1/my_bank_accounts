# Generated by Django 4.0.4 on 2022-05-19 18:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('categorization', '0002_category_periodicity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='periodicity',
        ),
    ]