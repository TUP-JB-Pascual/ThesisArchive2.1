# Generated by Django 5.0.6 on 2024-12-01 07:28

import website.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0020_thesis_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tempurl',
            name='pdf_file',
            field=models.FileField(max_length=500, upload_to='temporary_pdfs/'),
        ),
        migrations.AlterField(
            model_name='thesis',
            name='pdf_file',
            field=models.FileField(max_length=500, upload_to=website.models.rename_pdf),
        ),
    ]