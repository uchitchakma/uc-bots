from django.contrib import admin
from .models import User, JobLog

# Register your models here.

admin.site.register(User)
admin.site.register(JobLog)
