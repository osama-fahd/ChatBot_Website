from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse

from .forms import WorkoutForm
from .models import Workout, Set, Done

from routines.models import Routine

from exercises.models import Exercise

from django.contrib import messages


def new_workout_view(request: HttpRequest, routine_id: int):
    routine = Routine.objects.get(pk=routine_id)
    
    workout_form = WorkoutForm()

    if request.method == "POST":
        workout_form = WorkoutForm(request.POST)
        if workout_form.is_valid():
            workout = workout_form.save(commit=False)
            if request.POST["restTime"].isdigit():
                workout.restTime = int(request.POST["restTime"])
                workout.routine = routine
                workout.save()
                if request.POST.get("repetition", "").strip():
                    if request.POST['repetition'].isdigit():
                        weight = request.POST["weight"]
                        try:
                            weight = float(weight) 
                            if weight <= 0:
                                messages.error(request, "Weight must be a positive number.", "alert-danger")
                            else:
                                new_set = Set(weight=weight, repetition=int(request.POST['repetition']), workout=workout)
                                new_set.save()
                                messages.success(request, "Workout added successfully!", "alert-success")
                                
                        except ValueError:
                            messages.error(request, "Weight must be a valid number.", "alert-danger")
                    else:
                        messages.error(request, "Repetition must be digit number. Please correct the errors.", "alert-danger")
                else:
                    messages.error(request, "Repetition must be digit number. Please correct the errors.", "alert-danger")
            else:
                messages.error(request, "Rest Time must be digit number. Please correct the errors.", "alert-danger")
        else:
            messages.error(request, "There is an error in the form. Please correct the errors.", "alert-danger")
            
    else:
        messages.error(request, "There are no data received. Please correct the errors.", "alert-danger")

    return redirect("routines:routine_detail_view", routine_id=routine_id)


def update_workout_view(request:HttpRequest, workout_id:int):
    workout = Workout.objects.get(pk=workout_id)
    routine = Routine.objects.get(pk=workout.routine.id)
    exercises = Exercise.objects.all()

    if request.method == "POST":
        if request.POST["restTime"]:
            if request.POST["restTime"].isdigit():
                workout.restTime = int(request.POST["restTime"])
                workout.note = request.POST.get("note", "").strip()
                updated_exercise = Exercise.objects.get(pk=int(request.POST['exercise']))
                workout.exercise = updated_exercise
                workout.save()
                messages.success(request, "Updated Workout Successfuly!", "alert-success")
                return redirect("routines:routine_detail_view", routine_id=workout.routine.id)
            else:
                messages.error(request, "Rest Time must be digit number. Please correct the errors.", "alert-danger")
            
        else:
            messages.error(request, "There are no data received. Please correct the errors.", "alert-danger")

    return render(
        request,"workouts/update_workout.html",
        {
            "routine": routine,
            'workout':workout,
            'exercises': exercises,
        },
    )


def delete_workout_view(request:HttpRequest,  workout_id:int):
    try:
        workout = Workout.objects.get(pk=workout_id)
        workout.delete()
        messages.success(request, "Deleted Workout Successfuly!", "alert-success")
    except Exception as e:
        print(e)
        messages.error(request, "Couldn't Delete Workout!", "alert-danger")
    
    return redirect("main:home_view")


def new_set_view(request:HttpRequest, workout_id:int):
    
    if request.method == "POST":
        workout = Workout.objects.get(pk=workout_id)
                
        if request.POST['repetition'].isdigit():
            weight = request.POST["weight"]
            try:
                weight = float(weight) 
                if weight <= 0:
                    messages.error(request, "Weight must be a positive number.", "alert-danger")
                else:
                    new_set = Set(weight=weight, repetition=int(request.POST['repetition']), workout=workout)
                    new_set.save()
                    messages.success(request, "Added Set Successfuly!", "alert-success")
            except ValueError:
                messages.error(request, "Weight must be a valid number.", "alert-danger")
        else:
            messages.error(request, "Couldn't Add Set! Please insert correct numbers.", "alert-danger")
            
    else:
        messages.error(request, "Couldn't Add Set!. Please correct the errors.", "alert-danger")
    
    return redirect("routines:routine_detail_view", routine_id=workout.routine.id)




def update_set_view(request, set_id):
    if request.method == "POST":
        set_obj = Set.objects.get(pk=set_id)
        
        if request.POST['repetition'].isdigit():
            weight = request.POST["weight"]
            try:
                weight = float(weight) 
                if weight <= 0:
                    messages.error(request, "Weight must be a positive number.", "alert-danger")
                else:
                    set_obj.weight = weight
                    set_obj.repetition = request.POST['repetition']
                    set_obj.save()
                    messages.success(request, "The set updated successfully!", "alert-success")
            except ValueError:
                messages.error(request, "Weight must be a valid number.", "alert-danger")
        else:
            messages.error(request, "Repetition must be a digit.", "alert-danger")
           
    else:
        messages.error(request, "Couldn't Update Set!. Please correct the errors.", "alert-danger")

    return redirect("routines:routine_detail_view", routine_id=set_obj.workout.routine.id)


def delete_set_view(request:HttpRequest, set_id:int):
    try:
        set = Set.objects.get(pk=set_id)
        set.delete()
        messages.success(request, f"{set.workout.exercise.name} set {set.id} Deleted Successfuly!", "alert-success")
    except Exception as e:
        print(e)
        messages.error(request, "Couldn't Delete Set!", "alert-danger")
    
    return redirect("routines:routine_detail_view", routine_id=set.workout.routine.id)



def done_set_view(request: HttpRequest, set_id:int):
    workout_set = Set.objects.get(pk=set_id)
    try:

        done = Done.objects.filter(set=workout_set).first() 
        if not done:
            new_done = Done(set=workout_set)
            new_done.save()
            messages.success(request, "Set Done!", "alert-success")
        else:
            done.delete()
            messages.error(request, "Set Undone!", "alert-danger")

    except Set.DoesNotExist:
        messages.error(request, "Set not found.")
    except Exception as e:
        messages.error(request, "An error occurred: " + str(e))

    return redirect("routines:routine_detail_view", routine_id=workout_set.workout.routine.id)



def finish_workout_view(request: HttpRequest, workout_id: int):
    try:
        workout = Workout.objects.get(pk=workout_id)
        sets = workout.set_set.all()  

        for set_obj in sets:
            done = Done.objects.filter(set=set_obj).first()
            if done:
                done.delete()

        messages.success(request, f"All sets have been reset to 'Undone' for {workout.exercise.name} workout.", "alert-success")

    except Workout.DoesNotExist:
        messages.error(request, "Workout not found.", "alert-danger")
    except Exception as e:
        messages.error(request, f"An error occurred: {e}", "alert-danger")

    return redirect("routines:routine_detail_view", routine_id=workout.routine.id)



    
    
    


    
    
    