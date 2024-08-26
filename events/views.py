from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden, HttpResponse
from django.contrib import messages
from .models import Event, Registration
from .forms import RegistrationForm
import csv
from icalendar import Calendar, Event as CalendarEvent
from django.utils.timezone import localtime, make_aware
import datetime

def home(request):
    today = datetime.date.today()
    upcoming_events = Event.objects.filter(event_date__gte=today)
    past_events = Event.objects.filter(event_date__lt=today)
    return render(request, 'events/home.html', {
        'upcoming_events': upcoming_events,
        'past_events': past_events
    })

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    registered_teams_count = Registration.objects.filter(event=event).count()
    slots_left = event.max_teams - registered_teams_count
    total_slots = event.max_teams
    slot_fill_percentage = (1 - (slots_left / total_slots)) * 100
    
    return render(request, 'events/event_detail.html', {
        'event': event,
        'slots_left': slots_left,
        'slot_fill_percentage': slot_fill_percentage,
        'event_date': event.event_date,
        'event_time': event.event_time,
    })

def register(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    if event.registration_deadline < datetime.date.today():
        return HttpResponseForbidden("Registration deadline has passed.")
    
    registered_teams_count = Registration.objects.filter(event=event).count()
    
    if registered_teams_count >= event.max_teams:
        return HttpResponseForbidden("All slots are filled. Registration closed.")
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST, team_size=event.team_size)
        if form.is_valid():
            team_name = form.cleaned_data.get('team_name')
            
            # Check for duplicate VTU numbers
            members_data = [
                {
                    'name': form.cleaned_data[f'member{i}_name'],
                    'vtu_number': form.cleaned_data[f'member{i}_vtu_number'],
                    'year': form.cleaned_data[f'member{i}_year'],
                }
                for i in range(1, event.team_size + 1)
            ]
            
            duplicate_vtu_number = get_duplicate_vtu_number(event, members_data)
            if duplicate_vtu_number:
                messages.error(request, f"VTU number {duplicate_vtu_number} is already registered for this event.")
                return render(request, 'events/register.html', {
                    'form': form,
                    'event': event,
                })

            # Save the registration
            registration = Registration(
                event=event,
                team_name=team_name,
                members=members_data,  # Ensure this is properly formatted
                domain=form.cleaned_data.get('domain'),
                member1_email=form.cleaned_data.get('member1_email'),
            )
            registration.save()

            messages.success(request, "Registration successful!")
            return render(request, 'events/register.html', {
                'form': form,
                'event': event,
                'registration_complete': True,
                'whatsapp_group_link': event.whatsapp_group_link,
            })
        else:
            # If the form is not valid, the errors will be in form.errors
            messages.error(request, "Only @veltech.edu.in email addresses are allowed")
    
    else:
        form = RegistrationForm(team_size=event.team_size)
    
    return render(request, 'events/register.html', {'form': form, 'event': event})

def get_duplicate_vtu_number(event, members_data):
    registered_vtu_numbers = {member['vtu_number'] for registration in Registration.objects.filter(event=event) for member in registration.members}
    
    for member in members_data:
        if member['vtu_number'] in registered_vtu_numbers:
            return member['vtu_number']
    
    return None

def download_registrations_details(request, pk):
    event = get_object_or_404(Event, pk=pk)
    registrations = Registration.objects.filter(event=event)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="registrations_{event.title}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Team Name', 'Member Name', 'VTU Number', 'Year'])

    for registration in registrations:
        for member in registration.members:
            writer.writerow([
                registration.team_name,
                member['name'],
                member['vtu_number'],
                member['year'],
            ])

    return response

def add_to_calendar(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    event_datetime = datetime.datetime.combine(event.event_date, datetime.time.min)
    
    if not event_datetime.tzinfo:
        event_datetime = make_aware(event_datetime)

    cal = Calendar()

    cal_event = CalendarEvent()
    cal_event.add('summary', event.title)
    cal_event.add('dtstart', localtime(event_datetime))
    cal_event.add('dtend', localtime(event_datetime))
    cal_event.add('location', event.location)
    cal_event.add('description', event.description)

    cal.add_component(cal_event)

    response = HttpResponse(cal.to_ical(), content_type='text/calendar')
    response['Content-Disposition'] = f'attachment; filename="event_{event.id}.ics"'
    return response