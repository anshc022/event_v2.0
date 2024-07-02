from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden, HttpResponse
from .models import Event, Registration
from .forms import RegistrationForm
import csv
from icalendar import Calendar, Event as CalendarEvent
from django.utils.timezone import localtime, make_aware
from .models import Event  
import datetime

def home(request):
    today = datetime.date.today()
    upcoming_events = Event.objects.filter(registration_deadline__gte=today)
    past_events = Event.objects.filter(registration_deadline__lt=today)
    return render(request, 'events/home.html', {'upcoming_events': upcoming_events, 'past_events': past_events})

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    # Calculate number of registered teams for this event
    registered_teams_count = Registration.objects.filter(event=event).count()
    
    # Calculate available slots left
    slots_left = event.max_teams - registered_teams_count
    
    return render(request, 'events/event_detail.html', {
        'event': event,
        'slots_left': slots_left,
        'event_date': event.event_date,
        'event_time': event.event_time,
    })

def register(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if event.registration_deadline < datetime.date.today():
        return HttpResponseForbidden("Registration deadline has passed.")
    
    # Calculate number of registered teams for this event
    registered_teams_count = Registration.objects.filter(event=event).count()
    
    # Check if all slots are filled
    if registered_teams_count >= event.max_teams:
        return HttpResponseForbidden("All slots are filled. Registration closed.")
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST, team_size=event.team_size)
        if form.is_valid():
            members_data = []
            for i in range(1, event.team_size + 1):
                member_data = {
                    'name': form.cleaned_data[f'member{i}_name'],
                    'vtu_number': form.cleaned_data[f'member{i}_vtu_number'],
                    'year': form.cleaned_data[f'member{i}_year'],
                }
                members_data.append(member_data)
            
            registration = Registration(
                event=event,
                team_name=form.cleaned_data['team_name'],
                members=members_data,
            )
            registration.save()

            # Set registration_complete to True to trigger the popup
            registration_complete = True

            return render(request, 'events/register.html', {'form': form, 'event': event, 'registration_complete': registration_complete})
    else:
        form = RegistrationForm(team_size=event.team_size)
    
    return render(request, 'events/register.html', {'form': form, 'event': event})

def download_registrations_details(request, pk):
    event = Event.objects.get(pk=pk)
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
    # Get the event object
    event = get_object_or_404(Event, id=event_id)

    # Ensure event_date is a datetime object and make it timezone-aware if it's naive
    event_datetime = datetime.datetime.combine(event.event_date, datetime.time.min)
    
    if not event_datetime.tzinfo:  # Check if event_datetime is naive
        event_datetime = make_aware(event_datetime)  # Make it timezone-aware

    # Create a new iCalendar instance
    cal = Calendar()

    # Create an event
    cal_event = CalendarEvent()
    cal_event.add('summary', event.title)
    cal_event.add('dtstart', localtime(event_datetime))
    cal_event.add('dtend', localtime(event_datetime))
    cal_event.add('location', event.location)  # Optional: Add event location
    cal_event.add('description', event.description)  # Optional: Add event description

    # Add event to calendar
    cal.add_component(cal_event)

    # Return response with .ics file
    response = HttpResponse(cal.to_ical(), content_type='text/calendar')
    response['Content-Disposition'] = f'attachment; filename="event_{event.id}.ics"'
    return response