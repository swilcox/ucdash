from models import Job, JobGroup
from django.contrib import admin



class JobAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class JobGroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}



admin.site.register(Job,JobAdmin)
admin.site.register(JobGroup,JobGroupAdmin)
