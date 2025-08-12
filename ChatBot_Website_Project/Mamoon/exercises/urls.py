from django.urls import path
from . import views


app_name = "exercises"

urlpatterns = [
    path("all/", views.all_exercises_view, name="all_exercises_view"),
    path("details/<exercise_id>/", views.exercise_detail_view, name="exercise_detail_view"),
    path("new/exercise/", views.new_exercise_view, name="new_exercise_view"),
    path("update/<exercise_id>/", views.update_exercise_view, name="update_exercise_view"),
    path("delete/<exercise_id>/", views.delete_exercise_view, name="delete_exercise_view"),
    path("search/exercises/", views.search_exercises_view, name="search_exercises_view"),
]
