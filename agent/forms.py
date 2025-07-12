from django import forms
from .models import VoteReport, Incident

class VoteReportForm(forms.ModelForm):
    class Meta:
        model = VoteReport
        fields = [
            'poll_name', 'valid_vote', 'spoilt_vote', 
            'vote_count', 'photo', 'dr_form', 'comment',
            'location'
        ]
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
        }

class IncidentReportForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = [
            'location', 'incident_type', 'description', 'location_description',
            'photo', 'is_urgent'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'incident_type': forms.Select(attrs={'class': 'form-select'}),
        }

class CandidateLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class AgentLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)