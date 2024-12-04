from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Event 
from christians.models import Christian




@login_required(login_url='/authentication/login')
def event_index(request):
    events = Event.objects.filter(owner=request.user)

    # Paginate events
    paginator = Paginator(events, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'events': events,
        'page_obj': page_obj,
    }

    return render(request, 'events/index.html', context)


@login_required(login_url='/authentication/login')
def add_event(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        date = request.POST.get('date')
        description = request.POST.get('description', '').strip()
        location = request.POST.get('location', '').strip()

        if not name:
            messages.error(request, 'Name is required.')
            return render(request, 'events/addEvent.html', {'values': request.POST})

        Event.objects.create(
            name=name,
            date=date,
            description=description,
            location=location,
            owner=request.user
        )
        messages.success(request, 'Event added successfully.')
        return redirect('events')

    return render(request, 'events/addEvent.html', {'values': request.POST})


@login_required(login_url='/authentication/login')
def event_edit(request, id):
    event = get_object_or_404(Event, pk=id, owner=request.user)

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        date = request.POST.get('date')
        description = request.POST.get('description', '').strip()
        location = request.POST.get('location', '').strip()

        if not name:
            messages.error(request, 'Name is required.')
            return render(request, 'events/editEvent.html', {'event': event, 'values': request.POST})

        event.name = name
        event.date = date
        event.description = description
        event.location = location
        event.save()

        messages.success(request, 'Event updated successfully.')
        return redirect('events')

    return render(request, 'events/editEvent.html', {'event': event, 'values': event})


@login_required(login_url='/authentication/login')
def delete_event(request, id):
    event = get_object_or_404(Event, pk=id, owner=request.user)
    event.delete()
    messages.success(request, 'Event removed.')
    return redirect('events')

@login_required(login_url='/authentication/login')
def analytics(request):
    event_count = Event.objects.count()  # Get the number of events
    christian_count = Christian.objects.count()  # Get the number of Christians or similar entity
    context = {
        'event_count': event_count,
        'christian_count': christian_count,
    }
    return render(request, 'events/analytics.html', context)
