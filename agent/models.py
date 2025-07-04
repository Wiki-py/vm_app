from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    party = models.CharField(max_length=100)
    constituency = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='candidates/', null=True, blank=True)
    party_symbol = models.ImageField(upload_to='party_symbols/', null=True, blank=True)
    party = models.CharField(max_length=100, default='Independent')
    constituency = models.CharField(max_length=100, default='Unknown')
    position = models.CharField(max_length=100, default='Candidate')
    
    def __str__(self):
        return f"{self.user.username} ({self.party})"

class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='Agent')
    agent_nin = models.CharField(max_length=20, unique=True, blank=True, null=True)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='agents', null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.username} (Agent for {self.candidate.user.username})"

class PollingStation(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    constituency = models.CharField(max_length=100)
    registered_voters = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.name}, {self.location}"

class VoteReport(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='vote_report', null=True, blank=True  )
    poll_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    valid_vote = models.IntegerField(default=0)
    spoilt_vote = models.IntegerField(default=0)
    vote_count = models.IntegerField(default=0)
    comment = models.TextField(blank=True)
    photo = models.ImageField(upload_to='vote_reports/', null=True, blank=True)
    dr_form = models.FileField(upload_to='dr_forms/')
    submitted_at = models.DateTimeField(default=timezone.now)
    
    def percentage_of_valid(self):
        if self.valid_votes > 0:
            return round((self.vote_count / self.valid_vote) * 100, 1)
        return 0
    
    def __str__(self):
        return self.agent.user.username if self.agent else "Vote Report"

class Incident(models.Model):
    INCIDENT_TYPES = [
        ('late_open', 'Late Opening'),
        ('missing_materials', 'Missing Materials'),
        ('voter_intimidation', 'Voter Intimidation'),
        ('ballot_stuffing', 'Ballot Stuffing'),
        ('technical_issue', 'Technical Issue'),
        ('other', 'Other'),
    ]
    
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='incidents', null=True, blank=True)
    polling_station = models.ForeignKey(PollingStation, on_delete=models.CASCADE, default=None, null=True, blank=True)
    incident_type = models.CharField(max_length=50, choices=INCIDENT_TYPES)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='incidents/', null=True, blank=True)
    is_urgent = models.BooleanField(default=False)
    resolved = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.incident_type
    
#class Report(models.Model):
    #agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='reports', default=None, null=True, blank=True)
    #polling_station = models.ForeignKey(PollingStation, on_delete=models.CASCADE, default=None, null=True, blank=True)
    #description = models.TextField(blank=True)
    #photo = models.ImageField(upload_to='DRforms/', null=True, blank=True)
    #submitted_at = models.DateTimeField(default=timezone.now)
    #location = models.CharField(max_length=200, blank=True)
    
    #def __str__(self):
        #return self.polling_station.name if self.polling_station else "General Report"

class Region(models.Model):
    name = models.CharField(max_length=100)
    total_voters = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name

class ResultSummary(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='result_summaries', null=True, blank=True)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, blank=True)
    polling_station = models.ForeignKey(PollingStation, on_delete=models.CASCADE, related_name='pollingstation', null=True, blank=True)
    votes = models.IntegerField(default=0)
    percentage = models.FloatField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Result Summaries"
    
    def __str__(self):
        location = self.region if self.region else self.polling_station
        return f"{self.candidate.user.username} - {location} - {self.votes} votes"