# Generated by Django 4.0.4 on 2022-05-19 21:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            'categorization',
            '0007_rename_category_keywords_categorykeywords_category',
        ),
    ]

    operations = [
        migrations.RenameField(
            model_name='categorykeywords',
            old_name='Keyword',
            new_name='keyword',
        ),
    ]
