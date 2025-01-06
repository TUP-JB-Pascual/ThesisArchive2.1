# Generated by Django 5.0.6 on 2025-01-05 15:08

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0042_alter_tempurl_expiration_date'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='tempurl',
            name='expiration_date',
            field=models.DateTimeField(default=datetime.datetime(2025, 1, 5, 23, 8, 16, 279378)),
        ),
        migrations.AlterField(
            model_name='thesis',
            name='poster',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='thesis', to=settings.AUTH_USER_MODEL),
        ),
    ]
