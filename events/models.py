from django.db import models
from django.utils import timezone

class Coordinator(models.Model):
    name = models.CharField(max_length=100)
    vtu_number = models.CharField(max_length=10)
    image_link = models.URLField()

    def __str__(self):
        return self.name

class StudentCoordinator(models.Model):
    name = models.CharField(max_length=100)
    year = models.CharField(max_length=50)
    is_ieee_member = models.BooleanField(default=False)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    image_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=200)
    banner_image = models.URLField(default="paste banner link here")
    event_link = models.URLField(default="paste event link here")
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
    coordinators = models.ManyToManyField(Coordinator)
    whatsapp_group_link = models.URLField(null=True, blank=True)
    student_coordinators = models.ManyToManyField(StudentCoordinator, related_name='events', blank=True)

    def __str__(self):
        return self.title

    def registration_open(self):
        return self.registration_deadline >= timezone.now().date()

    def registration_deadline_passed(self):
        return not self.registration_open()

class Registration(models.Model):
    DOMAIN_CHOICES = [
        ('iot', 'IoT'),
        ('full_stack', 'Full Stack'),
        ('ai_ml', 'AI/ML'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    team_name = models.CharField(max_length=100)
    members = models.JSONField(default=list)  # Use Django's built-in JSONField with a default value
    domain = models.CharField(max_length=20, choices=DOMAIN_CHOICES, blank=True, null=True)  # Field for domain
    member1_email = models.EmailField(blank=True, null=True)  # Email for the first member

    def __str__(self):
        return self.team_name
