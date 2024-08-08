# Generated by Django 4.2.7 on 2024-08-08 09:48

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coordinator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('vtu_number', models.CharField(max_length=10)),
                ('image_link', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('banner_image', models.URLField(default='paste banner link here')),
                ('event_link', models.URLField(default='paste event link here')),
                ('location', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('general_rules', models.TextField(default='• Participants must adhere to the theme announced at the beginning of the event.\n• All assets used in the game (art, music, etc.) must either be original or properly attributed.\n• Teams can have a maximum of 3 members.\n• Games must be submitted before the deadline to be eligible for judging.')),
                ('additional_information', models.TextField(default='All participants will receive a Participation Certificate.\nWinners will receive a Merit Certificate.\nAll participants will receive On-Duty (OD) status.')),
                ('event_date', models.DateField(default=django.utils.timezone.now)),
                ('event_time', models.TimeField(default=django.utils.timezone.now)),
                ('prizes', models.TextField(default='1st Place: [Prize]\n2nd Place: [Prize]\n3rd Place: [Prize]')),
                ('max_teams', models.IntegerField(default=10)),
                ('team_size', models.IntegerField(default=3)),
                ('registration_deadline', models.DateField()),
                ('whatsapp_group_link', models.URLField(blank=True, null=True)),
                ('coordinators', models.ManyToManyField(to='events.coordinator')),
            ],
        ),
        migrations.CreateModel(
            name='StudentCoordinator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('year', models.CharField(max_length=50)),
                ('is_ieee_member', models.BooleanField(default=False)),
                ('contact_number', models.CharField(blank=True, max_length=15, null=True)),
                ('image_link', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=100)),
                ('members', models.JSONField(default=list)),
                ('domain', models.CharField(default='Not Specified', max_length=100)),
                ('member1_email', models.EmailField(blank=True, default='no-reply@example.com', max_length=254, null=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.event')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='student_coordinators',
            field=models.ManyToManyField(blank=True, related_name='events', to='events.studentcoordinator'),
        ),
    ]
