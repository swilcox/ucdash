from models import SpecialJob, SpecialJobAttributeValue
from django.contrib import admin


class SpecialJobAdmin(admin.ModelAdmin):
    pass

admin.site.register(SpecialJob, SpecialJobAdmin)

