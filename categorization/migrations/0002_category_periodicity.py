# Generated by Django 4.0.4 on 2022-05-19 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categorization', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='periodicity',
            field=models.CharField(choices=[('unique', 'Unique'), ('monthly', 'Mensuel'), ('once_a_year', 'Une fois par an'), ('twice_a_year', 'Deux fois par an')], default='unique', max_length=50),
        ),
    ]