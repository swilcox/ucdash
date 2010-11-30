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
    result = models.BooleanField()
    result_code = models.IntegerField()
    job = models.ForeignKey(Job)
    at = models.DateTimeField()
    info = models.TextField()

    def __unicode__(self):
        return self.name


