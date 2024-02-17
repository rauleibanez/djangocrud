from django.contrib import admin
from .models import Task

# esta clase es para  poder ver los campos 
# de solo lectura dentro de la interfaz del 
# administador
class TaskAdmin(admin.ModelAdmin):
    readonly_fields=('created',)

# Register your models here.
admin.site.register(Task, TaskAdmin)