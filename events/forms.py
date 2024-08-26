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
    def __init__(self, *args, **kwargs):
        team_size = kwargs.pop('team_size', 3)  # Default to 3 if not provided
        super().__init__(*args, **kwargs)

        # Add fields for each team member
        self.fields['team_name'] = forms.CharField(max_length=100, label='Team Name')
        for i in range(1, team_size + 1):
            member_label = f'Member {i} Name'
            if i == 1:
                member_label += ' (Team Leader)'
                self.fields[f'member{i}_name'] = forms.CharField(max_length=100, label=member_label)
                self.fields['member1_email'] = forms.EmailField(label='Member 1 Email ID')
                self.fields['member1_mobile_number'] = forms.CharField(
                    max_length=15,
                    label='Member 1 Mobile Number',
                    required=True
                )
            else:
                self.fields[f'member{i}_name'] = forms.CharField(max_length=100, label=member_label)
                self.fields[f'member{i}_vtu_number'] = forms.CharField(max_length=20, label=f'Member {i} VTU Number')
                self.fields[f'member{i}_year'] = forms.IntegerField(label=f'Member {i} Year')

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
        fields = [
            'team_name',
            'member1_name',
            'member1_email',
            'member1_mobile_number'
        ]  # Include all required fields

        # Include other fields as necessary for your use case
