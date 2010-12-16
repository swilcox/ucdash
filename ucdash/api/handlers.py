from piston.handler import BaseHandler
from piston.utils import rc
from piston.utils import require_extended
from jobs.models import Notification, NotificationExtra, Job
from datetime import datetime
import socket

class JobNotificationHandler(BaseHandler):
    allowed_methods = ('POST',)
    model = Notification
    
    def create(self, request, job_slug=None):

        if request.content_type and job_slug:
            try:
                j = Job.objects.get(slug=job_slug)
            except:
                print "couldn't find job"
                return rc.BAD_REQUEST
            em = self.model(result=request.data['result'], log=request.data['log'], job=j)
            if 'duration' in request.data:
                em.duration = request.data['duration']
            if 'remote_host' not in request.data:
                try:
                    em.remote_host = socket.gethostbyaddr(request.META.get('REMOTE_ADDR',''))[0]
                except:
                    em.remote_host = ''
            em.remote_ip = request.META.get('REMOTE_ADDR','')
            em.save()
            if 'extra' in request.data:
                for e in request.data['extra']:
                    ex = NotificationExtra(notification=em)
                    ex.field_name = e
                    ex.field_value = str(request.data['extra'][e])
                    ex.save()

            return rc.CREATED
        else:
            return rc.BAD_REQUEST

