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

        self.fields['team_name'] = forms.CharField(max_length=100, label='Team Name')
        self.fields['member1_email'] = forms.EmailField(label='Member 1 Email ID')
        self.fields['member1_mobile_number'] = forms.CharField(
            max_length=15,
            label='Member 1 Mobile Number',
            required=True
        )

        # Add fields for each team member
        for i in range(1, team_size + 1):
            self.fields[f'member{i}_name'] = forms.CharField(max_length=100, label=f'Member {i} Name')
            self.fields[f'member{i}_vtu_number'] = forms.CharField(max_length=20, label=f'Member {i} VTU Number')
            self.fields[f'member{i}_year'] = forms.IntegerField(label=f'Member {i} Year')

        # Add a link field
        self.fields['link'] = forms.URLField(label='Link', required=False)

    def clean_member1_email(self):
        email = self.cleaned_data.get('member1_email')
        if email and not email.endswith('@veltech.edu.in'):
            raise ValidationError('Only @veltech.edu.in email addresses are allowed.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        self.clean_member1_email()
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        members = [
            {
                'name': self.cleaned_data.get(f'member{i}_name'),
                'vtu_number': self.cleaned_data.get(f'member{i}_vtu_number'),
                'year': self.cleaned_data.get(f'member{i}_year'),
                'email': self.cleaned_data.get('member1_email') if i == 1 else '',
                'mobile_number': self.cleaned_data.get('member1_mobile_number') if i == 1 else '',
            }
            for i in range(1, self.instance.event.team_size + 1)
        ]
        instance.members = members
        if commit:
            instance.save()
        return instance

    class Meta:
        model = Registration
        fields = ['team_name', 'member1_email', 'member1_mobile_number', 'link']  # Include the new link field
