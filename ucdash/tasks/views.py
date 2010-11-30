from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Job, JobGroup

def dashboard(request):
    job_groups = JobGroup.objects.all()
    jobs = Job.objects.all()
    return render_to_response('dashboard.html',{'jobs':jobs,'job_groups':job_groups},context_instance=RequestContext(request))
