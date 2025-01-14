# Generated by Django 5.0.6 on 2025-01-05 16:57

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0046_alter_tempurl_expiration_date_alter_tempurl_id_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tempurl',
            name='expiration_date',
            field=models.DateTimeField(default=datetime.datetime(2025, 1, 6, 0, 57, 45, 606811)),
        ),
        migrations.AlterField(
            model_name='tempurl',
            name='id_pic',
            field=models.ImageField(default=1, upload_to='request_id/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]),
            preserve_default=False,
        ),
    ]
