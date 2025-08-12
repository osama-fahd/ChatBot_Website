from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse

from .models import Exercise, Step
from .forms import ExerciseForm

from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from django.db import IntegrityError, transaction

from django.contrib import messages


def all_exercises_view(request:HttpRequest):
    exercises = Exercise.objects.all()
    workout_categories = Exercise.WorkoutCategory.choices
    
    page_number = request.GET.get("page", 1)
    paginator = Paginator(exercises, 4)
    exercises_page = paginator.get_page(page_number)
    
    return render(request, "exercises/all_exercises.html", {'exercises': exercises_page, 'workout_categories': workout_categories})

def exercise_detail_view(request:HttpRequest, exercise_id:int):
    exercise = Exercise.objects.get(pk=exercise_id)
    
    return render(request, "exercises/exercise_detail.html", {'exercise': exercise})


def new_exercise_view(request:HttpRequest):

    if not request.user.is_staff:
        messages.success(request, "Only staff can add exercises!", "alert-warning")
        return redirect("main:home_view")

    if request.method == 'POST':
        exercise = Exercise.objects.create(
            name=request.POST['name'],
            description=request.POST.get('description', ''),
            image=request.FILES.get('image'),
            video_link=request.POST.get('video_link', ''),
            video=request.FILES.get('video'),
            workout_category=request.POST['workout_category'],
            equipment_category=request.POST['equipment_category'],
            exercise_category=request.POST['exercise_category'],
        )

        exercise.save()
        messages.success(request, "Exercise added!", "alert-warning")
        return redirect('exercises:all_exercises_view')  

    return render(request, 'exercises/new_exercise.html')


def new_instruction_view(request:HttpRequest, exercise_id:int):

    if not request.user.is_staff:
        messages.success(request, "Only staff can add instructions!", "alert-warning")
        return redirect("main:home_view")

    if request.method == 'POST':
        exercise = Exercise.objects.get(pk=exercise_id)
        instruction = Step.objects.create(
            exercise=exercise,
            instruction=request.POST['instruction']
        )

        instruction.save()
        messages.success(request, "instruction added!", "alert-warning")  

    return redirect('exercises:exercise_detail_view',exercise_id=exercise_id)


def update_exercise_view(request:HttpRequest, exercise_id:int):

    pass

def delete_exercise_view(request:HttpRequest,  exercise_id:int):
    if not request.user.is_staff:
        messages.success(request, "Only staff can delete exercises!", "alert-warning")
        return redirect("main:home_view")
    
    try:
        exercise = Exercise.objects.get(pk=exercise_id)
        exercise.delete()
        messages.success(request, "Deleted Exercise Successfuly!", "alert-success")
    except Exception as e:
        print(e)
        messages.error(request, "Couldn't Delete Exercise!", "alert-danger")
    
    return redirect("main:home_view")


def search_exercises_view(request:HttpRequest):
    workout_categories = Exercise.WorkoutCategory.choices
    exercises = Exercise.objects.all()  

    filter_by = None
    
    if "search" in request.GET and len(request.GET["search"]) >= 3:
        exercises = Exercise.objects.filter(name__icontains=request.GET["search"])
    
            
    if "filter_workout_category" in request.GET and request.GET["filter_workout_category"] != '':
        exercises = exercises.filter(workout_category=request.GET['filter_workout_category'])
        filter_by = request.GET['filter_workout_category']
    
    if not exercises.exists():
        messages.error(request, "Couldn't Find Exercise!", "alert-danger")
        exercises = []
    
    return render(request, "exercises/exercise_search.html", {'exercises': exercises, 
                                                              'workout_categories': workout_categories, 
                                                              'filter_by':filter_by})

    
    
    


    
    
    