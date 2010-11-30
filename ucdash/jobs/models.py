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
    jobs = models.ManyToManyRel(Job)

    def __unicode__(self):
        return self.name


class Notification(models.Model):
    result_code = models.IntegerField()
    job = models.ForeignKey(Job)
    at = models.DateTimeField(auto_now_add=True,null=True,blank=True,db_index=True)
    start_time = models.DateTimeField(null=True,blank=True)
    end_time = models.DateTimeField(null=True,blank=True)
    run_time = models.IntegerField(null=True,blank=True)
    output_text = models.TextField(blank=True)
    errout_text = models.TextField(blank=True)

    def __unicode__(self):
        return 'result: %s for job: %s' % (str(self.result_code), str(self.job))


class NotificationExtra(models.Model):
    notification = models.ForeignKey(Notification)
    field_name = models.CharField(max_length=50)
    field_value = models.TextField()

    def __unicode__(self):
        return self.field_name + ': ' + self.field_value[:100]

