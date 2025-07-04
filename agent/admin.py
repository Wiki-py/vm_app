from django.contrib import admin
from .models import ResultSummary, Region, PollingStation,  Agent, Candidate, Incident, VoteReport

#admin.site.register(Device)
#admin.site.register(Candidate)
#admin.site.register(Agent)
#admin.site.register(Report)

@admin.register(VoteReport)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['agent','location']

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ['user','position', 'photo', 'party', 'constituency']

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'candidate']

@admin.register(Incident)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['agent', 'submitted_at']


@admin.register(Region)
class Region(admin.ModelAdmin):
    list_display = ['name']

@admin.register(PollingStation)
class PollingStation(admin.ModelAdmin):
    list_display = ['name', 'constituency']

@admin.register(ResultSummary)
class ResultSummary(admin.ModelAdmin):
    list_display = ['candidate', 'polling_station']






