# Generated by Django 4.0.4 on 2022-05-19 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categorization', '0003_remove_category_periodicity'),
    ]

    operations = [
        migrations.CreateModel(
            name='Periodicity',
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
                ('name', models.CharField(max_length=50)),
            ],
        ),
    ]
