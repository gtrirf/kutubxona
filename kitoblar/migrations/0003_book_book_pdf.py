# Generated by Django 5.0.6 on 2024-08-05 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kitoblar', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='book_pdf',
            field=models.FileField(blank=True, null=True, upload_to='pdf_files/'),
        ),
    ]
