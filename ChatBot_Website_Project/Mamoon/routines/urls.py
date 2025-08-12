from django.urls import path
from . import views


app_name = "routines"

urlpatterns = [
    path("all/", views.all_routines_view, name="all_routines_view"),
    path("new/routine/", views.new_routine_view, name="new_routine_view"),
    path("update/<routine_id>/", views.update_routine_view, name="update_routine_view"),
    path("delete/<routine_id>/", views.delete_routine_view, name="delete_routine_view"),
    path("detail/<routine_id>", views.routine_detail_view, name="routine_detail_view"),
    path("search/routines/", views.search_routines_view, name="search_routines_view"),
]