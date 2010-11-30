from django.db import models


class Job(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    description = models.TextField()

    def __unicode__(self):
        return str(self.name)


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
    start_time = models.DateTimeField(null=True,blank=True)
    end_time = models.DateTimeField(null=True,blank=True)
    duration = models.IntegerField(null=True,blank=True)
    log = models.TextField(blank=True)

    def __unicode__(self):
        return 'result: %s for job: %s' % (str(self.result), str(self.job))


class NotificationExtra(models.Model):
    notification = models.ForeignKey(Notification,related_name='extra_info')
    field_name = models.CharField(max_length=50,db_index=True)
    field_value = models.TextField()

    def __unicode__(self):
        return self.field_name + ': ' + self.field_value[:100]

