# Generated by Django 5.0.6 on 2025-01-05 19:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0051_alter_tempurl_expiration_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tempurl',
            name='expiration_date',
            field=models.DateTimeField(default=datetime.datetime(2025, 1, 6, 3, 25, 17, 931012)),
        ),
        migrations.AlterField(
            model_name='tempurl',
            name='status',
            field=models.CharField(choices=[('Approved', 'Approved'), ('Rejected', 'Rejected'), ('Pending', 'Pending')], default='Pending', max_length=10),
        ),
    ]
