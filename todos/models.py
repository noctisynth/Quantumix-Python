from django.db import models


class Permission(models.Model):
    name = models.CharField("权限标识", max_length=10)
    level = models.IntegerField("权限位格")
    desc = models.TextField("权限描述", max_length=128)
    create_time = models.DateTimeField("设立时间", auto_now_add=True)
    update_time = models.DateTimeField("更新时间", auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "权限"
        verbose_name_plural = "权限"


class User(models.Model):
    username = models.CharField("用户名", max_length=12, unique=True)
    password = models.CharField("密码", max_length=128)
    nickname = models.CharField("用户昵称", max_length=8, blank=True)
    permission = models.ForeignKey(
        Permission, verbose_name="权限", default=0, on_delete=models.CASCADE
    )
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("更新时间", auto_now=True)

    def __str__(self) -> str:
        return self.nickname or self.username

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"


class Project(models.Model):
    user = models.ForeignKey(
        User,
        name="uid",
        verbose_name="负责人",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    name = models.CharField("项目名称", max_length=10)
    permission = models.ForeignKey(
        Permission, verbose_name="权限", default=0, on_delete=models.DO_NOTHING
    )
    priority = models.IntegerField("优先级")
    content = models.TextField("项目内容", max_length=128)
    start_time = models.DateTimeField("起始时间", blank=True, null=True)
    end_time = models.DateTimeField("终止时间", blank=True, null=True)
    is_checked = models.BooleanField("结项状态", blank=True, null=True)
    create_time = models.DateTimeField("立项时间", auto_now_add=True)
    update_time = models.DateTimeField("更新时间", auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "项目"
        verbose_name_plural = "项目"


class Todo(models.Model):
    project = models.ForeignKey(
        Project,
        verbose_name="项目",
        name="pid",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    user = models.ForeignKey(
        User,
        name="uid",
        verbose_name="负责人",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    name = models.CharField("待办事项", max_length=10)
    permission = models.ForeignKey(
        Permission, verbose_name="权限", default=0, on_delete=models.DO_NOTHING
    )
    priority = models.IntegerField("优先级")
    content = models.TextField("待办内容", max_length=128)
    desc = models.TextField("注释", max_length=128, blank=True, null=True)
    startline = models.DateTimeField("起始时间", blank=True, null=True)
    endline = models.DateTimeField("死线", blank=True, null=True)
    parent = models.ForeignKey(
        "self",
        name="tid",
        verbose_name="父进程",
        related_name="child",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    is_checked = models.BooleanField("完成状态")
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("更新时间", auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "待办事项"
        verbose_name_plural = "待办事项"


class Task(models.Model):
    project = models.ForeignKey(
        Project,
        verbose_name="项目",
        name="pid",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    user = models.ForeignKey(
        User,
        name="uid",
        verbose_name="负责人",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    name = models.CharField("任务名", max_length=10)
    permission = models.ForeignKey(
        Permission, verbose_name="权限", default=0, on_delete=models.DO_NOTHING
    )
    priority = models.IntegerField("优先级")
    content = models.TextField("任务内容", max_length=128)
    desc = models.TextField("注释", max_length=128, blank=True, null=True)
    start_time = models.DateTimeField("起始时间", blank=True, null=True)
    duration = models.DurationField("终止时间", blank=True, null=True)
    parent = models.ForeignKey(
        "self",
        name="tid",
        verbose_name="父进程",
        related_name="child",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    is_checked = models.BooleanField("完成状态", default=False)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("更新时间", auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "待办任务"
        verbose_name_plural = "待办任务"
