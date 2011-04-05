from django.db import models
from jobs.models import Job


SPECIAL_JOB_TYPES = (('DS','Daily Store'),
                     ('WS','Weekly Store'),
                     ('BWS','Bi-Weekly Store'),
                     ('MS','Monthly Store'),
                     ('RS','Random Store'),
                     ('DM','Daily Machine'),
                     ('RM','Random Machine'),
                    )


class SpecialJob(models.Model):
    job = models.ForeignKey(Job,related_name='special_info')
    job_type = models.CharField(max_length=4,choices=SPECIAL_JOB_TYPES)

    def __unicode__(self):
        return str(self.job) + " (%s)" % str(self.job_type)

    @models.permalink
    def get_absolute_url(self):
        return ('specialjobs.views.special_job', (),{'job_slug':self.job.slug})


class SpecialJobAttributeValue(models.Model):
    special_job = models.ForeignKey(SpecialJob)
    attrib_field = models.CharField(max_length=20)
    attrib_value = models.CharField(max_length=255,blank=True)

    def __unicode__(self):
        return "Job: %s  attribute: %s--> %s" % (str(self.special_job), str(self.attrib_field), str(self.attrib_value))

