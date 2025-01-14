# Generated by Django 5.0.6 on 2024-10-24 18:18

import website.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_rename_water_pdf_thesis_watermark_pdf'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thesis',
            name='abstract_pdf',
        ),
        migrations.RemoveField(
            model_name='thesis',
            name='watermark_pdf',
        ),
        migrations.AlterField(
            model_name='thesis',
            name='pdf_file',
            field=models.FileField(max_length=256, upload_to=website.models.rename_pdf),
        ),
    ]
