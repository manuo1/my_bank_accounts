# Generated by Django 4.0.4 on 2022-06-03 21:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categorization', '0019_alter_categorykeyword_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionWithoutStatement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('label', models.CharField(max_length=255)),
                ('value', models.DecimalField(decimal_places=2, max_digits=20)),
                ('extended_label', models.CharField(blank=True, max_length=255)),
                ('custom_label', models.CharField(blank=True, max_length=255)),
                ('fitid', models.CharField(max_length=255)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='categorization.category')),
            ],
        ),
    ]
