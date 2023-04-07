# Generated by Django 4.1.7 on 2023-04-07 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cedula', models.CharField(max_length=255)),
                ('id_audiencia', models.CharField(max_length=255)),
                ('id_comparendo', models.CharField(max_length=255)),
                ('video', models.URLField(blank=True)),
                ('fecha_subida', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
