# Generated by Django 4.2.7 on 2024-08-01 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_alter_registration_domain'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='domain',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
