from models import MetricDefinition
from django.contrib import admin


class MetricDefinitionAdmin(admin.ModelAdmin):
    pass




admin.site.register(MetricDefinition, MetricDefinitionAdmin)


