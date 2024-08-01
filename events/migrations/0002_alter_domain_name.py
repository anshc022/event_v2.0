# Generated by Django 4.2.7 on 2024-08-01 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domain',
            name='name',
            field=models.CharField(choices=[('FS', 'Full Stack'), ('AI', 'AI & ML'), ('IOT', 'IoT')], max_length=100, unique=True),
        ),
    ]
