from django.db import models
from jobs.models import Job

CHART_TYPES = [('line','Line'),]

class MetricDefinition(models.Model):
    name = models.CharField(max_length=50,db_index=True)
    field_names = models.CharField(max_length=50,db_index=True,help_text='comma-delimited list of field names')
    regex = models.TextField(blank=True,help_text='regular expression to find (by name) the values for the fields')
    max_display_entries = models.IntegerField()
    chart_type = models.CharField(max_length=100,choices=CHART_TYPES,default='line')
    data_label = models.CharField(max_length=100,blank=True,help_text='what to call the data on the graph')
    jobs = models.ManyToManyField(Job,related_name='metrics',help_text='jobs that use this metric')

    def __unicode__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        #override save() just in case we need to do some tweaking as part of saving...
        super(MetricDefinition, self).save(*args, **kwargs) # Call the "real" save() method.
        