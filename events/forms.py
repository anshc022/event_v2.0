# forms.py

from django import forms
from .models import Registration
from django import forms
from .models import Event

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
        team_size = kwargs.pop('team_size', 3)  # default to 3 if not provided
        super().__init__(*args, **kwargs)
        
        self.fields['team_name'] = forms.CharField(max_length=100, label='Team Name')
        for i in range(1, team_size + 1):
            self.fields[f'member{i}_name'] = forms.CharField(max_length=100, label=f'Member {i} Name')
            self.fields[f'member{i}_vtu_number'] = forms.CharField(max_length=20, label=f'Member {i} VTU Number')
            self.fields[f'member{i}_year'] = forms.IntegerField(label=f'Member {i} Year')

    class Meta:
        model = Registration
        fields = ['team_name']  # Include team_name field here if you want to save it in the model
