# Generated by Django 5.0.6 on 2024-08-08 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='telegram_profile_photo',
            field=models.URLField(blank=True, default='https://thumbs.dreamstime.com/b/default-avatar-profile-icon-vector-social-media-user-image-182145777.jpg', null=True),
        ),
    ]
