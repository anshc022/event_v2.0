# Generated by Django 4.2.7 on 2024-08-01 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_alter_registration_domain'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='domain',
            field=models.CharField(default='Not Specified', max_length=100),
        ),
    ]
