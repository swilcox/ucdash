from django.db import models
from jobs.models import Job, Notification


class MetricDefinition(models.Model):
    name = models.CharField(max_length=50,db_index=True)
    field_names = models.CharField(max_length=50,db_index=True,help_text='comma-delimited list of field names')
    required = models.BooleanField()
    client_supplied = models.BooleanField()
    regex = models.TextField(blank=True)
    max_display_entries = models.IntegerField()
    chart_type = models.CharField(max_length=100,blank=True)
    jobs = models.ManyToManyField(Job,related_name='metrics',help_text='jobs that use this metric')

    def __unicode__(self):
        return str(self.name)
    
