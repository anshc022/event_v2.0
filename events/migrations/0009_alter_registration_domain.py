# Generated by Django 4.2.7 on 2024-08-01 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_alter_registration_domain_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='domain',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]