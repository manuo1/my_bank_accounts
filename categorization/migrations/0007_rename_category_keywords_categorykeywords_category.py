# Generated by Django 4.0.4 on 2022-05-19 21:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('categorization', '0006_remove_category_category_keywords_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='categorykeywords',
            old_name='category_keywords',
            new_name='category',
        ),
    ]
