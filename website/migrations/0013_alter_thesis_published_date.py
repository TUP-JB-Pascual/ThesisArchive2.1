# Generated by Django 5.0.6 on 2024-11-17 16:47

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0012_alter_tempurl_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thesis',
            name='published_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]