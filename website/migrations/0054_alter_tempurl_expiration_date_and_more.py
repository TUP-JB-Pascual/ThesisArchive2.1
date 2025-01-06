# Generated by Django 5.0.6 on 2025-01-05 19:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0053_alter_tempurl_expiration_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tempurl',
            name='expiration_date',
            field=models.DateTimeField(default=datetime.datetime(2025, 1, 6, 3, 30, 57, 193656)),
        ),
        migrations.AlterField(
            model_name='tempurl',
            name='url_status',
            field=models.CharField(choices=[('Expired', 'Expired'), ('Used', 'Used'), ('Valid', 'Valid'), ('Does Not Exist', 'Does Not Exist')], default='Does Not Exist', max_length=15),
        ),
    ]
