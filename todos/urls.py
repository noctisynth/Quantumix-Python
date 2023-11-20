from django.urls import path
from .views import (
    login,
    new_task,
    new_project,
    new_todo,
    take_project,
    take_task,
    get_project,
    get_task,
    get_todo,
    finish_project,
    finish_task,
    finish_todo,
)

urlpatterns = [
    # 登录
    path("login/", login),
    # 新建
    path("project/new/", new_project),
    path("task/new/", new_task),
    path("todo/new/", new_todo),
    # 接取
    path("project/take/", take_project),
    path("task/take/", take_task),
    # 捕获
    path("project/get/", get_project),
    path("task/get/", get_task),
    path("todo/get/", get_todo),
    # 结项
    path("project/finish/", finish_project),
    path("task/finish/", finish_task),
    path("todo/finish/", finish_todo),
]
