from models import Job, JobGroup, Notification, JobConfig
from django.contrib import admin


class JobConfigInline(admin.StackedInline):
    model = JobConfig

class JobAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    inlines = [JobConfigInline,]

class JobGroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class NotificationAdmin(admin.ModelAdmin):
    pass



admin.site.register(Job,JobAdmin)
admin.site.register(JobGroup,JobGroupAdmin)
admin.site.register(Notification,NotificationAdmin)
