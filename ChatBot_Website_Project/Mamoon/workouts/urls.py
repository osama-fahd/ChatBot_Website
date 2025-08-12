from django.urls import path
from . import views


app_name = "workouts"

urlpatterns = [
    path("new/workout/<routine_id>", views.new_workout_view, name="new_workout_view"),
    path("update/<workout_id>/", views.update_workout_view, name="update_workout_view"),
    path("delete/<workout_id>/", views.delete_workout_view, name="delete_workout_view"),
    
    path("sets/new/<workout_id>", views.new_set_view, name="new_set_view"),
    path("sets/update/<set_id>/", views.update_set_view, name="update_set_view"),
    path("sets/delete/<set_id>/", views.delete_set_view, name="delete_set_view"),
    path("checks/add/<set_id>/", views.done_set_view, name="done_set_view"),
    path("checks/finsh/<workout_id>/", views.finish_workout_view, name="finish_workout_view"),
]