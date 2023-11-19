from django.urls import path
from .views import new_task, new_project, new_todo, take_project, take_task

urlpatterns = [
    path("project/new/", new_project),
    path("task/new/", new_task),
    path("todo/new/", new_todo),
    path("project/take/", take_project),
    path("task/new/", take_task),
]
