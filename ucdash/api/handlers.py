from piston.handler import BaseHandler
from piston.utils import rc
from piston.utils import require_extended
from jobs.models import Notification, NotificationExtra, Job

class JobNotificationHandler(BaseHandler):
    allowed_methods = ('POST',)
    model = Notification

    @require_extended
    def create(self, request, job_slug=None):
        if request.content_type and job_slug:
            print job_slug
            try:
                j = Job.objects.get(slug=job_slug)
            except:
                return rc.BAD_REQUEST
            data = request.data
            print data
            em = self.model(result=data['result'], log=data['log'])
            if 'duration' in data:
                em.duration = data['duration']
            if 'start_time' in data:
                em.start_time = data['start_time']
            if 'end_time' in data:
                em.end_time = data['end_time']
            em.save()

            return rc.CREATED
        else:
            return rc.BAD_REQUEST

