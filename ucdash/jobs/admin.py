from models import Job, JobGroup, Notification
from django.contrib import admin


class JobAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class JobGroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class NotificationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Job,JobAdmin)
admin.site.register(JobGroup,JobGroupAdmin)
admin.site.register(Notification,NotificationAdmin)
