# Generated by Django 4.2.11 on 2024-03-12 10:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_book_langue'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='langue',
            new_name='language',
        ),
    ]