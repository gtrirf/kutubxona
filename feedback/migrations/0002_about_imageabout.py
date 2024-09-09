# Generated by Django 5.0.6 on 2024-08-08 13:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('theme', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'about',
            },
        ),
        migrations.CreateModel(
            name='ImageAbout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('about', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feedback.about')),
            ],
            options={
                'db_table': 'imagesforabout',
            },
        ),
    ]
