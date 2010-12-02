from piston.handler import BaseHandler
from piston.utils import rc
from piston.utils import require_extended
from jobs.models import Notification, NotificationExtra, Job
from datetime import datetime

class JobNotificationHandler(BaseHandler):
    allowed_methods = ('POST',)
    model = Notification

    
    def create(self, request, job_slug=None):
        print request
        if request.content_type and job_slug:
            print job_slug
            print request.data
            try:
                j = Job.objects.get(slug=job_slug)
            except:
                print "couldn't find job"
                return rc.BAD_REQUEST
            data = request.data
            print data
            em = self.model(result=data['result'], log=data['log'], job=j)
            if 'duration' in data:
                em.duration = data['duration']
            em.save()

            return rc.CREATED
        else:
            return rc.BAD_REQUEST

