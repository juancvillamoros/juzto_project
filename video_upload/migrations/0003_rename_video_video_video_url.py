# Generated by Django 4.1.7 on 2023-04-15 23:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video_upload', '0002_video_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video',
            old_name='video',
            new_name='video_url',
        ),
    ]
