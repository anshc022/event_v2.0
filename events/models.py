from django.db import models
from django.utils import timezone

class Coordinator(models.Model):
    name = models.CharField(max_length=100)
    vtu_number = models.CharField(max_length=10)
    image_link = models.URLField()

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=200)
    banner_image = models.URLField(default="paste banner link here")
    event_link = models.URLField(default="paste banner link here ")
    location = models.CharField(max_length=200)
    description = models.TextField()
    general_rules = models.TextField(default="• Participants must adhere to the theme announced at the beginning of the event.\n• All assets used in the game (art, music, etc.) must either be original or properly attributed.\n• Teams can have a maximum of 3 members.\n• Games must be submitted before the deadline to be eligible for judging.")
    additional_information = models.TextField(default="All participants will receive a Participation Certificate.\nWinners will receive a Merit Certificate.\nAll participants will receive On-Duty (OD) status.")
    event_date = models.DateField(default=timezone.now)
    event_time = models.TimeField(default=timezone.now)
    prizes = models.TextField(default="1st Place: [Prize]\n2nd Place: [Prize]\n3rd Place: [Prize]")
    max_teams = models.IntegerField(default=10)
    team_size = models.IntegerField(default=3)
    registration_deadline = models.DateField()
    coordinators = models.ManyToManyField('Coordinator')
    whatsapp_group_link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title

    def registration_open(self):
        return self.registration_deadline >= timezone.now().date()

    def registration_deadline_passed(self):
        return not self.registration_open()

class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    team_name = models.CharField(max_length=100)
    members = models.JSONField(default=list)  # Use Django's built-in JSONField with a default value

    def __str__(self):
        return self.team_name
