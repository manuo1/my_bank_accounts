# Generated by Django 4.0.4 on 2022-05-23 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categorization', '0016_delete_transactiondata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorykeyword',
            name='keyword',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]