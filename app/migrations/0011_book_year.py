# Generated by Django 5.0.6 on 2024-06-24 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_remove_book_categories_book_semester_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='year',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]