# Generated by Django 4.2.7 on 2024-09-30 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_remove_registration_domain_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='additional_form_fields',
            field=models.JSONField(blank=True, default=dict),
        ),
    ]