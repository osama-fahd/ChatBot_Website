from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse

# from .forms import RoutineForm
from .models import Routine

from django.contrib.auth.models import User

from workouts.models import Workout, Set, Done

from exercises.models import Exercise

from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from django.db import transaction
from django.utils import timezone
    

def all_routines_view(request:HttpRequest):
    if not request.user.is_authenticated:
        messages.warning(request, "Only registered users can see their routines", "alert-warning")
        return redirect("main:home_view")
        
        
    routines = Routine.objects.filter(user=request.user)
        
    page_number = request.GET.get("page", 1)
    paginator = Paginator(routines, 4)
    routines_page = paginator.get_page(page_number)
    
    return render(request, "routines/all_routines.html", {'routines': routines_page})
    
def profile_view(request:HttpRequest, user_id:int):
    user = User.objects.get(pk=user_id)
    routines = Routine.objects.filter(user=user, is_public=True)
        
    return render(request, "routines/profile.html", {'routines': routines, 'user':user})


def routine_detail_view(request:HttpRequest, routine_id:int):
    routine = Routine.objects.get(pk=routine_id)
    
    exercises = Exercise.objects.all()
    checks = Done.objects.all()
    
    workouts = routine.workout_set.all()
    
    return render(request, "routines/routine_details.html", {'routine': routine,
                                                             'checks': checks, 
                                                             'exercises':exercises,
                                                             'workouts': workouts})

@login_required
def new_routine_view(request:HttpRequest):
    
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        is_public = request.POST.get("is_public") == "1"  
        
        if name:
            with transaction.atomic():
                routine:Routine = Routine(user=request.user, name=request.POST['name'], is_public=is_public)
                routine.save()
                messages.success(request, "Continue To Add Your Workouts!", "alert-success")
                return redirect("routines:routine_detail_view", routine_id=routine.id)
        else:
            print("not valid form", routine.errors)
            messages.error(request, "Couldn't Able To Add The title!", "alert-danger")
    
    return render(request, "routines/new_routine.html")

@login_required
def update_routine_view(request, routine_id):
    routine = Routine.objects.get(pk=routine_id)

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        is_public = request.POST.get("is_public") == "1" 

        if name:
            with transaction.atomic():
                routine.name = name
                routine.is_public = is_public
                routine.save()
                messages.success(request, "Routine updated successfully!", "alert-success")
                return redirect("routines:routine_detail_view", routine_id=routine.id)
        else:
            messages.error(request, "Couldn't update the routine title!", "alert-danger")

    return render(request, "routines/update_routine.html", {'routine': routine})
    

@login_required
def delete_routine_view(request:HttpRequest,  routine_id:int):
    try:
        routine = Routine.objects.get(pk=routine_id)
        routine.delete()
        messages.success(request, "Deleted Routine Successfully!", "alert-success")
    except Exception as e:
        print(e)
        messages.error(request, "Couldn't Delete Routine!", "alert-danger")
    
    return redirect("routines:all_routines_view")


def search_routines_view(request:HttpRequest):
    if "search" in request.GET and len(request.GET["search"]) >= 3:
        routines = Routine.objects.filter(name__icontains=request.GET["search"])
    
    else:
        messages.error(request, "Couldn't Find Routine!", "alert-danger")
        routines = []
    
    return render(request, "routines/search_routine.html", {'routines': routines,})

    
    
    


    
    
    