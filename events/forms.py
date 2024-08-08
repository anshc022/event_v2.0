from django import forms
from .models import Registration, Event
from django.core.exceptions import ValidationError

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'general_rules': forms.Textarea(attrs={'rows': 4}),
            'prizes': forms.Textarea(attrs={'rows': 4}),
        }

class RegistrationForm(forms.ModelForm):
    domain = forms.CharField(
        max_length=100, 
        required=True, 
        label='Domain (e.g., IoT, Full Stack, AI/ML)', 
        help_text='Specify the domain for your registration (e.g., IoT, Full Stack, AI/ML)'
    )

    def __init__(self, *args, **kwargs):
        team_size = kwargs.pop('team_size', 3)  # Default to 3 if not provided
        super().__init__(*args, **kwargs)

        self.fields['team_name'] = forms.CharField(max_length=100, label='Team Name')

        # Add fields for each team member
        for i in range(1, team_size + 1):
            self.fields[f'member{i}_name'] = forms.CharField(max_length=100, label=f'Member {i} Name')
            self.fields[f'member{i}_vtu_number'] = forms.CharField(max_length=20, label=f'Member {i} VTU Number')
            self.fields[f'member{i}_year'] = forms.IntegerField(label=f'Member {i} Year')

        # Add email field only for the first member
        if team_size > 0:
            self.fields['member1_email'] = forms.EmailField(label='Member 1 Email ID')

    def clean_member1_email(self):
        email = self.cleaned_data.get('member1_email')

        if email and not email.endswith('@veltech.edu.in'):
            raise ValidationError('Only @veltech.edu.in email addresses are allowed.')
        
        return email

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('member1_email')

        # Call clean_member1_email to validate the email
        self.clean_member1_email()

        return cleaned_data

    class Meta:
        model = Registration
        fields = ['team_name', 'domain', 'member1_email']  # Include team_name, domain, and member1_email fields here

# forms.py
from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['overall_organization', 'relevance_of_content', 'satisfaction_with_time_venue', 'interest_level', 'expectations_met', 'opinion_on_speakers', 'usefulness', 'overall_effectiveness', 'additional_comments']
        widgets = {
            'additional_comments': forms.Textarea(attrs={'rows': 4}),
        }

    overall_organization = forms.ChoiceField(choices=[
        ('Excellent', 'Excellent'),
        ('Very Good', 'Very Good'),
        ('Good', 'Good'),
        ('Average', 'Average'),
    ], label='How was the overall organization of the event?')

    relevance_of_content = forms.ChoiceField(choices=[
        ('Excellent', 'Excellent'),
        ('Very Good', 'Very Good'),
        ('Good', 'Good'),
        ('Average', 'Average'),
    ], label='How relevant was the content presented during the event?')

    satisfaction_with_time_venue = forms.ChoiceField(choices=[
        ('Excellent', 'Excellent'),
        ('Very Good', 'Very Good'),
        ('Good', 'Good'),
        ('Average', 'Average'),
    ], label='Are you satisfied with the time and venue?')

    interest_level = forms.ChoiceField(choices=[
        ('Excellent', 'Excellent'),
        ('Very Good', 'Very Good'),
        ('Good', 'Good'),
        ('Average', 'Average'),
    ], label='How interesting was the event for you?')

    expectations_met = forms.ChoiceField(choices=[
        ('Excellent', 'Excellent'),
        ('Very Good', 'Very Good'),
        ('Good', 'Good'),
        ('Average', 'Average'),
    ], label='Did the event meet your expectations?')

    opinion_on_speakers = forms.ChoiceField(choices=[
        ('Excellent', 'Excellent'),
        ('Very Good', 'Very Good'),
        ('Good', 'Good'),
        ('Average', 'Average'),
    ], label='What is your opinion about the speakers/presenters?')

    usefulness = forms.ChoiceField(choices=[
        ('Excellent', 'Excellent'),
        ('Very Good', 'Very Good'),
        ('Good', 'Good'),
        ('Average', 'Average'),
    ], label='How useful was the event from a knowledge and information perspective?')

    overall_effectiveness = forms.ChoiceField(choices=[
        ('Excellent', 'Excellent'),
        ('Very Good', 'Very Good'),
        ('Good', 'Good'),
        ('Average', 'Average'),
    ], label='Overall effectiveness of the event')

    additional_comments = forms.CharField(widget=forms.Textarea, required=False, label='Additional comments and suggestions for future events:')