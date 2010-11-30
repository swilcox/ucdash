from django.db import models


STATUS_CHOICES = [('','Unknown'),
                  ('A','Okay'),
                  ('C','Complete'),
                  ('X','Error'),
                  ('W','Warning'),
                  ('L','Late'),
                  ('M','Missing'),
                  ('R','Running')]


class Job(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    description = models.TextField()
    options = models.TextField()
    latest_status = models.CharField(max_length=1,choices=STATUS_CHOICES,default='',blank=True)

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
    at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    start_time = models.DateTimeField(null=True,blank=True)
    end_time = models.DateTimeField(null=True,blank=True)
    run_time = models.BigIntegerField(null=True,blank=True)
    output_text = models.TextField()
    errout_text = models.TextField()

    def __unicode__(self):
        return self.name


class NotificationExtra(models.Model):
    notification = models.ForeignKey(Notification)
    field_name = models.CharField(max_length=50)
    field_value = models.TextField()

    def __unicode__(self):
        return self.field_name + ': ' + self.field_value[:100]

