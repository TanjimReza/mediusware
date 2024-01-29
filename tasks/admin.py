from django.contrib import admin
from .models import Task, TaskUser, TaskPhoto
# Register your models here.
admin.site.register(Task)
admin.site.register(TaskUser)
admin.site.register(TaskPhoto)

