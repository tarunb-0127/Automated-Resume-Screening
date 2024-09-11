from django.contrib import admin
from .models import CustomUser,JobPosting,Application

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(JobPosting)
admin.site.register(Application)

