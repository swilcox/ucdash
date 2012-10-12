from django.db import models
from django.utils.datetime_safe import date
from datetime import timedelta


JOB_FREQUENCY = (
  ('DAILY','Daily'),
  )
    #for now we're keeping the list of JOB_FREQUENCY short... not sure what can easily be supported / when...

class Job(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    description = models.TextField()
    frequency = models.CharField(max_length=10,choices=JOB_FREQUENCY,blank=True,help_text="how often the job is run")
    multipart_field = models.CharField(max_length=50,blank=True,help_text="extra field to use when determining which part of a multi-part job is being reported")
    multipart_names = models.TextField(blank=True,help_text="comma-delimited list of names for each part of the job")
    display_extra_fields = models.TextField(blank=True,help_text="comma-delimited list of extra fields to display")

    def multipart_flag(self):
        return len(self.multipart_field) > 0

    def multipart_status(self,query_date=None,**kwargs):
        all_parts = set([n.strip() for n in str(self.multipart_names).split(',')])
        if query_date is None:
            query_date = date.today()
        qs = self.notifications.filter(at__gt=query_date,at__lt=date.fromordinal(query_date.toordinal() + 1),extra_info__field_name=self.multipart_field)
        good_parts = qs.filter(result=0)
        error_parts = qs.exclude(result=0)
        missing_parts = all_parts.difference(set([n.extra_info.get(field_name=self.multipart_field).field_value for n in qs if n.extra_info.get(field_name=self.multipart_field)]))
        return {'good_parts':good_parts,'error_parts':error_parts,'missing_parts':missing_parts,'all_parts':all_parts}

    def multipart_status_previous(self,**kwargs):
        return self.multipart_status(query_date=(date.today() - timedelta(days=1)))
    
    def extra_display_fields_list(self):
        return [ef.strip() for ef in self.display_extra_fields.split(',')]

    @models.permalink
    def get_absolute_url(self):
        return ('jobs.views.job', (self.slug,), {})

    def __unicode__(self):
        return str(self.name)


class JobGroup(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    jobs = models.ManyToManyField(Job, related_name='groups')

    def __unicode__(self):
        return self.name


class MultiPartNotificationManager(models.Manager):
    def good_parts(self):
        super(MultiPartNotificationManager, self).get_query_set().filter(result=0)

    def error_parts(self):
        super(MultiPartNotificationManager, self).get_query_set().filter(result__ne=0)


class Notification(models.Model):
    result = models.IntegerField()
    job = models.ForeignKey(Job,related_name='notifications')
    at = models.DateTimeField(auto_now_add=True,null=True,blank=True,db_index=True)
    duration = models.IntegerField(null=True,blank=True)
    log = models.TextField(blank=True)
    remote_ip = models.IPAddressField(blank=True,db_index=True)
    remote_host = models.CharField(max_length=255,blank=True,db_index=True)
    objects = MultiPartNotificationManager()
    
    class Meta:
        get_latest_by = 'at'
        ordering = ['-at']

    def __unicode__(self):
        return 'result: %s for job: %s' % (str(self.result), str(self.job))

    def save(self, *args, **kwargs):
        #override save() just in case we need to do some tweaking as part of saving...
        super(Notification, self).save(*args, **kwargs) # Call the "real" save() method.

    @models.permalink
    def get_absolute_url(self):
        return ('jobs.views.notification_detail', (self.id,), {})


class NotificationExtra(models.Model):
    notification = models.ForeignKey(Notification,related_name='extra_info')
    field_name = models.CharField(max_length=50,db_index=True)
    field_value = models.TextField()

    def __unicode__(self):
        return self.field_name + ': ' + self.field_value[:100]


