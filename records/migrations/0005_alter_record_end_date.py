# Generated by Django 5.1 on 2024-11-10 02:55

import records.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0004_alter_record_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='end_date',
            field=models.DateTimeField(default=records.models.next_year),
        ),
    ]