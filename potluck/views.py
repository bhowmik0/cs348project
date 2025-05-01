from django.shortcuts import render, redirect, get_object_or_404
from .models import PotluckEvent, DishSignup
from .forms import PotluckEventForm, DishSignupForm
from django.db.models import Count, Avg
from .models import RSVP
from django.db import connection
from datetime import date
from .forms import ReportFilterForm
from django.db import transaction


def event_report(request):
    print("event_report view loaded")

    form = ReportFilterForm(request.GET or None)

    print("Form is bound:", form.is_bound)
    print("Form is valid:", form.is_valid())
    print("Form errors:", form.errors)

    results = []
    stats = {
        'total_events': 0,
        'avg_dishes': 0,
        'most_common_category': None,
    }


    if form.is_valid():
        start_date = form.cleaned_data['start_date'] or date(2000, 1, 1)
        end_date = form.cleaned_data['end_date'] or date(2100, 1, 1)
        organizer = form.cleaned_data['organizer']

        with connection.cursor() as cursor:
            query = """
                SELECT e.id, e.title, e.date, COUNT(d.id) as dish_count
                FROM potluck_potluckevent e
                LEFT JOIN potluck_dishsignup d ON e.id = d.event_id
                WHERE e.date BETWEEN %s AND %s
            """
            params = [start_date, end_date]

            if organizer:
                query += " AND e.organizer_id = %s"
                params.append(organizer.id)

            query += " GROUP BY e.id, e.title, e.date ORDER BY e.date"

            cursor.execute(query, params)
            results = cursor.fetchall()
            print("Results:", results)

        # Compute additional stats
        event_count = len(results)
        total_dishes = sum(r[3] for r in results)

        stats['total_events'] = event_count
        stats['avg_dishes'] = round(total_dishes / event_count, 2) if event_count > 0 else 0

        # Bonus: Most common category
        with connection.cursor() as cursor:
            category_query = """
                SELECT category, COUNT(*) as count
                FROM potluck_dishsignup d
                JOIN potluck_potluckevent e ON e.id = d.event_id
                WHERE e.date BETWEEN %s AND %s
            """
            cat_params = [start_date, end_date]

            if organizer:
                category_query += " AND e.organizer_id = %s"
                cat_params.append(organizer.id)

            category_query += " GROUP BY category ORDER BY count DESC LIMIT 1"

            cursor.execute(category_query, cat_params)
            cat_result = cursor.fetchone()
            if cat_result:
                stats['most_common_category'] = cat_result[0]

    return render(request, 'potluck/report.html', {
        'form': form,
        'results': results,
        'stats': stats
    })

def event_list(request):
    events = PotluckEvent.objects.all()
    return render(request, 'potluck/event_list.html', {'events': events})

def event_create(request):
    if request.method == 'POST':
        form = PotluckEventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = PotluckEventForm()
    return render(request, 'potluck/event_form.html', {'form': form})

def event_edit(request, pk):
    event = get_object_or_404(PotluckEvent, pk=pk)
    if request.method == 'POST':
        form = PotluckEventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = PotluckEventForm(instance=event)
    return render(request, 'potluck/event_form.html', {'form': form})

def event_delete(request, pk):
    event = get_object_or_404(PotluckEvent, pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    return render(request, 'potluck/event_confirm_delete.html', {'event': event})

def dish_signup_create(request, event_id=None):
    if request.method == 'POST':
        form = DishSignupForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                form.save()
                #raise Exception("Simulating error - rollback test")
            return redirect('dish_signup_list')
    else:
        form = DishSignupForm()
        if event_id:
            form.fields['event'].initial = event_id
    return render(request, 'potluck/dish_signup_form.html', {'form': form})

def dish_signup_list(request):
    signups = DishSignup.objects.all()
    return render(request, 'potluck/dish_signup_list.html', {'signups': signups})

def dish_signups_for_event(request, event_id):
    event = get_object_or_404(PotluckEvent, pk=event_id)
    signups = DishSignup.objects.filter(event=event)
    return render(request, 'potluck/dish_signup_event.html', {
        'event': event,
        'signups': signups
    })
