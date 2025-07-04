from django.shortcuts import render, redirect
from django.db import models
from django.db.models import Sum, ExpressionWrapper, F, FloatField
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import (
    Candidate, Agent, PollingStation, 
    VoteReport, Incident, ResultSummary, Region, #Report
)
from .forms import (
    VoteReportForm, IncidentReportForm,
    CandidateLoginForm, AgentLoginForm
)

def candidate_login(request):
    if request.method == 'POST':
        form = CandidateLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                try:
                    candidate = user.candidate
                    login(request, user)
                    return redirect('candidate_dashboard')
                except:
                    messages.error(request, "This account is not registered as a candidate")
            else:
                messages.error(request, "Invalid username or password")
    else:
        form = CandidateLoginForm()
    
    return render(request, 'candidate_login.html', {'form': form})

def agent_login(request):
    if request.method == 'POST':
        form = AgentLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                try:
                    agent = user.agent
                    login(request, user)
                    return redirect('agent_dashboard')
                except:
                    messages.error(request, "This account is not registered as an agent")
            else:
                messages.error(request, "Invalid username or password")
    else:
        form = AgentLoginForm()
    
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return render( request, 'logout.html')



@login_required
def candidate_dashboard(request):
    try:
        candidate = request.user.candidate
    except:
        return redirect('candidate_login')
    
    reports = VoteReport.objects.filter(agent__candidate=candidate).order_by('-submitted_at')
    incidents = Incident.objects.filter(agent__candidate=candidate, resolved=False).order_by('-submitted_at')
    
    vote_totals = VoteReport.objects.filter(
        agent__candidate=candidate
    ).aggregate(
        valid_vote=Sum('valid_vote'),
        vote_count=Sum('vote_count'),
        spoilt_vote=Sum('spoilt_vote')
    )
    
    context = {
        'reports': reports[:5],
        'total_votes': vote_totals['valid_vote'] or 0,
        'candidate_votes': vote_totals['vote_count'] or 0,
        'spoilt_votes': vote_totals['spoilt_vote'] or 0,
        'active_incidents_count': incidents.count(),
        # ... other context
    }
    

    return render(request, 'candidate_dashboard.html', context)

@login_required
def agent_dashboard(request):
    try:
        agent = request.user.agent
    except:
        return redirect('login')
    
    reports = VoteReport.objects.filter(agent=agent).count()
    incidents = Incident.objects.filter(agent=agent, resolved=False).count()
    
    
    if request.method == 'POST':
        form = VoteReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.agent = agent
            report.save()
            messages.success(request, "Vote report submitted successfully!")
            return redirect('agent_dashboard')
    else:
        form = VoteReportForm()
    
    context = {
        'form': form,
        'reports_count': reports,
        'incidents_count': incidents,
    }
    return render(request, 'agent_dashboard.html', context)

@login_required
def report_incident(request):
    try:
        agent = request.user.agent
    except:
        return redirect('login')
    
    if request.method == 'POST':
        form = IncidentReportForm(request.POST, request.FILES)
        if form.is_valid():
            incident = form.save(commit=False)
            incident.agent = agent
            incident.save()
            messages.success(request, "Incident reported successfully!")
            return redirect('agent_dashboard')
    else:
        form = IncidentReportForm()
    
    context = {
        'form': form,
    }
    return render(request, 'incident.html', context)

@login_required
def reported_incidents(request):
    try:
        candidate = request.user.candidate
    except:
        return redirect('candidate_login')
    
    incidents = Incident.objects.filter(agent__candidate=candidate).order_by('-submitted_at')
    urgent_count = incidents.filter(is_urgent=True, resolved=False).count()
    resolved_count = incidents.filter(resolved=True).count()
    
    context = {
        'incidents': incidents,
        'urgent_count': urgent_count,
        'resolved_count': resolved_count,
    }
    return render(request, 'reported_incidents.html', context)

@login_required
def results_summary(request):
    try:
        candidate = request.user.candidate
    except:
        return redirect('candidate_login')
    
    # Get all reports for this candidate
    reports = VoteReport.objects.filter(agent__candidate=candidate)
    
    # Calculate totals
    total_stations = PollingStation.objects.count()
    reported_stations = reports.values('poll_name').distinct().count()
    total_votes = models.Sum(report.valid_vote for report in reports)
    candidate_votes = models.Sum(report.vote_count for report in reports)
    spoilt_votes = models.Sum(report.spoilt_vote for report in reports)
    
    # Get top performing areas
    top_areas = reports.values(
    'poll_name', 
    'location'
).annotate(
    votes=Sum('vote_count'),
    valid_votes=Sum('valid_vote')
).annotate(
    percentage=ExpressionWrapper(
        F('votes') * 100.0 / F('valid_votes'),
        output_field=FloatField()
    )
).order_by('-votes')[:5]
    
    # Get regional breakdown
    regions = Region.objects.annotate(
        votes=models.Sum('resultsummary__votes', filter=models.Q(resultsummary__candidate=candidate)),
        percentage=models.Avg('resultsummary__percentage', filter=models.Q(resultsummary__candidate=candidate))
    )
    
    # Get polling stations data
    polling_stations = reports.values(
        'poll_name', 
        'id'
    ).annotate(
        votes=models.Sum('vote_count'),
        percentage=ExpressionWrapper(
        F('votes') * 100.0 / F('valid_vote'),
        output_field=FloatField())
    ).order_by('-votes')[:10]
    
    # Get candidate comparison data
    #candidates = Candidate.objects.annotate(
        #votes=models.Sum('agents__votereport__candidate_votes'),
        #percentage=models.Avg('agent__votereport__percentage_of_valid')
    #).order_by('-votes')
    
    # Mark which candidate is the current user
    #for c in candidates:
        #c.is_you = (c == candidate)
    
    context = {
        'total_stations': total_stations,
        'reported_stations': reported_stations,
        'total_votes': total_votes,
        'candidate_votes': candidate_votes,
        'spoilt_votes': spoilt_votes,
        'top_areas': top_areas,
        'regions': regions,
        'polling_stations': polling_stations,
        #'candidates': candidates,
    }
    return render(request, 'results.html', context)