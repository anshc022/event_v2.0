# Generated by Django 4.2.7 on 2024-08-01 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_alter_registration_domain'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='domain',
            field=models.CharField(blank=True, choices=[('IoT', 'IoT'), ('Full Stack', 'Full Stack'), ('AI/ML', 'AI/ML')], max_length=100, null=True),
        ),
    ]