# Generated by Django 5.0.6 on 2024-11-30 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0014_rename_author_thesis_poster'),
    ]

    operations = [
        migrations.AddField(
            model_name='thesis',
            name='authors',
            field=models.TextField(default='', max_length=255),
        ),
    ]