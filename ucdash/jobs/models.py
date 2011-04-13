from django.db import models


JOB_FREQUENCY = (
  ('DAILY','Daily'),
  ('WEEKLY','Weekly'),
  ('BIWEEKLY','Bi-Weekly'),
  ('MONTHLY','Monthly'),
  ('QUATERLY','Quaterly'),
  ('ANNUALLY','Annually'),
  ('SPORADIC','Sporadic'),
  )


class Job(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    description = models.TextField()

    @models.permalink
    def get_absolute_url(self):
        return ('jobs.views.job', (self.slug,), {})

    def __unicode__(self):
        return str(self.name)

    
class JobConfig(models.Model):
    job = models.OneToOneField(Job,related_name="config")
    frequency = models.CharField(max_length=10,choices=JOB_FREQUENCY,blank=True,help_text="how often the job is run")
    multipart_field = models.CharField(max_length=50,blank=True,help_text="extra field to use when determining which part of a multi-part job is being reported")
    multipart_names = models.TextField(blank=True,help_text="comma-delimited list of names for each part of the job")
    display_extra_fields = models.TextField(blank=True,help_text="comma-delimited list of extra fields to display in dashboard views")

    def __unicode__(self):
        return str(self.job) + " (config)"


class JobGroup(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    jobs = models.ManyToManyField(Job, related_name='groups')

    def __unicode__(self):
        return self.name


class Notification(models.Model):
    result = models.IntegerField()
    job = models.ForeignKey(Job,related_name='notifications')
    at = models.DateTimeField(auto_now_add=True,null=True,blank=True,db_index=True)
    duration = models.IntegerField(null=True,blank=True)
    log = models.TextField(blank=True)
    remote_ip = models.IPAddressField(blank=True,db_index=True)
    remote_host = models.CharField(max_length=255,blank=True,db_index=True)

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


