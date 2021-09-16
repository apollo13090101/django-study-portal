from django.contrib import admin
from dashboard.models import Homework, Note, Task


# Register your models here.
admin.site.register(Note)
admin.site.register(Homework)
admin.site.register(Task)
