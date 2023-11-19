from django.shortcuts import render, HttpResponse
from django.http import (
    HttpResponseNotAllowed,
    HttpResponseNotFound,
    HttpResponseForbidden,
    JsonResponse,
    # HttpResponseNotModified,
)
from django.core.handlers.wsgi import WSGIRequest
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict

from .models import Permission, Project, User, Todo, Task

import datetime
import re


def format_duration(duration):
    ...


@csrf_exempt
def login(request: WSGIRequest):
    username = request.POST.get("username")
    password = request.POST.get("password")
    search = User.objects.filter(username=username)
    if not search.count():
        return JsonResponse({"status": False, "message": "用户不存在!"})

    if search.first().password == password:
        request.session["username"] == username
        return JsonResponse({"status": True, "message": "登录成功！"})
    else:
        return JsonResponse({"status": True, "message": "密码错误！"})


@csrf_exempt
def new_project(request: WSGIRequest):
    if request.method == "GET":
        return HttpResponseNotAllowed("POST")

    username = request.POST.get("user")
    user = User.objects.filter(username=username).first()

    name = request.POST.get("name")

    level = request.POST.get("level")
    if Permission.objects.filter(level=level).count() == 0:
        return HttpResponseNotFound("权限不存在!")
    permission = Permission.objects.get(level=level)
    # elif Permission.objects.get(level=level) > workas.permission.level:
    #     return HttpResponseForbidden("权限不足, 拒绝访问.")

    priority = request.POST.get("priority")
    content = request.POST.get("content")
    start_time = request.POST.get("start_time")
    end_time = request.POST.get("end_time")

    Project.objects.create(
        uid=user,
        name=name,
        permission=permission,
        priority=priority,
        content=content,
        start_time=start_time,
        end_time=end_time,
        is_checked=False,
    )
    return HttpResponse("新项目创建成功!")


@csrf_exempt
def new_todo(request: WSGIRequest):
    if request.method == "GET":
        return HttpResponseNotAllowed("POST")

    pid = request.POST.get("project")
    project = Project.objects.filter(id=pid).first()
    # else:
    #     project = Project.objects.get(id=pid)
    #     if project.is_checked:
    #         return HttpResponseNotModified("目标项目已经结项!")

    username = request.POST.get("user")
    user = User.objects.filter(username=username).first()

    name = request.POST.get("name")

    level = request.POST.get("level")
    if Permission.objects.filter(level=level).count() == 0:
        return HttpResponseNotFound("权限不存在!")
    permission = Permission.objects.filter(level=level).first()
    # elif Permission.objects.get(level=level) > workas.permission.level:
    #     return HttpResponseForbidden("权限不足, 拒绝访问.")

    priority = request.POST.get("priority")
    content = request.POST.get("content")
    desc = request.POST.get("desc")
    startline = request.POST.get("startline")
    endline = request.POST.get("endline")
    if endline:
        try:
            match = re.match(r"^(?:(\d+) )?(\d+):(\d+):(\d+)$", endline)
            endline = datetime.timedelta(
                days=int(match.group(1)),
                hours=int(match.group(2)),
                minutes=int(match.group(3)),
                seconds=int(match.group(4)),
            )
        except:
            return JsonResponse({"status": False, "message": "错误的时间戳！"})
    tid = request.POST.get("parent")
    parent = Todo.objects.filter(id=tid).first()

    Todo.objects.create(
        pid=project,
        uid=user,
        name=name,
        permission=permission,
        priority=priority,
        content=content,
        desc=desc,
        startline=startline,
        endline=endline,
        tid=parent,
        is_checked=False,
    )
    return HttpResponse("新任务创建成功!")


@csrf_exempt
def new_task(request: WSGIRequest):
    if request.method == "GET":
        return HttpResponseNotAllowed("POST")

    pid = request.POST.get("project")
    project = Project.objects.filter(id=pid).first()
    # else:
    #     project = Project.objects.get(id=pid)
    #     if project.is_checked:
    #         return HttpResponseNotModified("目标项目已经结项!")

    username = request.POST.get("user")
    user = User.objects.filter(username=username).first()

    name = request.POST.get("name")

    level = request.POST.get("level")
    if Permission.objects.filter(level=level).count() == 0:
        return HttpResponseNotFound("权限不存在!")
    permission = Permission.objects.get(level=level)
    # elif Permission.objects.get(level=level) > workas.permission.level:
    #     return HttpResponseForbidden("权限不足, 拒绝访问.")

    priority = request.POST.get("priority")
    content = request.POST.get("content")
    desc = request.POST.get("desc")
    start_time = request.POST.get("start_time")
    duration = request.POST.get("duration")
    if duration:
        try:
            match = re.match(r"^(?:(\d+) )?(\d+):(\d+):(\d+)$", duration)
            duration = datetime.timedelta(
                days=int(match.group(1)),
                hours=int(match.group(2)),
                minutes=int(match.group(3)),
                seconds=int(match.group(4)),
            )
        except:
            return JsonResponse({"status": False, "message": "错误的时间戳！"})

    tid = request.POST.get("parent")
    parent = Task.objects.filter(id=tid).first()

    Task.objects.create(
        pid=project,
        uid=user,
        name=name,
        permission=permission,
        priority=priority,
        content=content,
        desc=desc,
        start_time=start_time,
        duration=duration,
        tid=parent,
        is_checked=False,
    )
    return HttpResponse("新任务创建成功!")


@csrf_exempt
def take_project(request: WSGIRequest):
    if request.method == "GET":
        return HttpResponseNotAllowed("POST")

    pid = request.POST.get("id")
    if pid and Project.objects.filter(id=pid).count() == 0:
        return HttpResponseNotFound("目标项目不存在!")
    project = Project.objects.get(id=pid)
    if project.user:
        return HttpResponseForbidden("目标项目已经被承接了.")

    Project.objects.filter(id=pid).update(
        user=User.objects.get(username=request.session.get("username"))
    )
    return HttpResponse("项目承接成功!")


@csrf_exempt
def take_task(request: WSGIRequest):
    if request.method == "GET":
        return HttpResponseNotAllowed("POST")

    pid = request.POST.get("id")
    if pid and Task.objects.filter(id=pid).count() == 0:
        return HttpResponseNotFound("目标项目不存在!")
    task = Task.objects.get(id=pid)
    if task.user:
        return HttpResponseForbidden("目标项目已经被承接了.")

    Task.objects.filter(id=pid).update(
        user=User.objects.get(username=request.session.get("username"))
    )
    return HttpResponse("任务承接成功!")


@csrf_exempt
def get_project(request: WSGIRequest):
    if request.method == "GET":
        return HttpResponseNotAllowed("POST")
    pid = request.POST.get("id")
    project = Project.objects.filter(id=pid).first()
    return (
        JsonResponse(model_to_dict(project))
        if project
        else JsonResponse({"status": False, "message": "目标项目不存在!"}, status_code=404)
    )


@csrf_exempt
def get_task(request: WSGIRequest):
    if request.method == "GET":
        return HttpResponseNotAllowed("POST")
    pid = request.POST.get("id")
    task = Task.objects.filter(id=pid).first()
    return (
        JsonResponse(model_to_dict(task))
        if task
        else JsonResponse({"status": False, "message": "目标项目不存在!"}, status_code=404)
    )


@csrf_exempt
def get_todo(request: WSGIRequest):
    if request.method == "GET":
        return HttpResponseNotAllowed("POST")
    pid = request.POST.get("id")
    todo = Todo.objects.filter(id=pid).first()
    return (
        JsonResponse(model_to_dict(todo))
        if todo
        else JsonResponse({"status": False, "message": "目标项目不存在!"}, status_code=404)
    )
