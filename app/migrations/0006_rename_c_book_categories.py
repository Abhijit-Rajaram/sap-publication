# Generated by Django 5.0.6 on 2024-06-12 14:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_remove_book_categories_book_c_alter_book_img'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='c',
            new_name='categories',
        ),
    ]