# Generated by Django 5.0.6 on 2024-06-22 17:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_order_is_delivered'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='categories',
        ),
        migrations.AddField(
            model_name='book',
            name='semester',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.RenameModel(
            old_name='Category',
            new_name='Degree',
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('degree', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.degree')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.department'),
        ),
    ]
