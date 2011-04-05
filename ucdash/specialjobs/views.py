from django.shortcuts import render_to_response
from django.template import RequestContext
#from models import Job, JobGroup, Notification
from django.utils.datetime_safe import date, datetime
from jobs.models import Job
from models import SpecialJob
from django.contrib.auth.decorators import login_required
import re


@login_required
def special_dashboard(request):
    #job_groups = JobGroup.objects.all()
    daily_store_jobs = Job.objects.filter(special_info__job_type='DS')
    for d in daily_store_jobs:
        d.todays_notifications = d.notifications.filter(at__gt=date.today())


    job_groups = {'Daily Store Jobs':daily_store_jobs}
    return render_to_response('special_dashboard.html',{'job_groups':job_groups},context_instance=RequestContext(request))
# Create your views here.


def special_job(request,job_slug=None,date_filter=None):
    if date_filter:
        start_date = datetime.strptime(date_filter,'%Y-%m-%d').date()
    else:
        start_date = date.today()
    end_date = date.fromordinal(start_date.toordinal() + 1)
    if job_slug:
        job = Job.objects.get(slug=job_slug)
        notifications = job.notifications.filter(at__gt=start_date,at__lt=end_date)
        for n in notifications:
            try:
                n.store = n.extra_info.get(field_name='store').field_value
            except Exception, ex:
                n.store = 'NA'
        metrics_data = {}
        return render_to_response('special_job.html',{'job':job,'metrics':metrics_data,'notifications':notifications,'host':request.get_host()},context_instance=RequestContext(request))
    else:
        return None
