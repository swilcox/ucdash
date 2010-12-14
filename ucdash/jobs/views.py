from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Job, JobGroup, Notification
import re


def dashboard(request):
    job_groups = JobGroup.objects.all()
    jobs = Job.objects.all()
    return render_to_response('dashboard.html',{'jobs':jobs,'job_groups':job_groups},context_instance=RequestContext(request))


def notification_detail(request,notification_id=None):
    if notification_id:
        notification = Notification.objects.get(id=notification_id)
    else:
        notification = None
    return render_to_response('notification_detail.html',{'notification':notification},context_instance=RequestContext(request))


def job(request,job_slug=None):
    if job_slug:
        job = Job.objects.get(slug=job_slug)
        job_metrics = job.metrics.all()
        metrics_data = {}
        for jm in job_metrics:
            notifications = job.notifications.all()[:jm.max_display_entries].reverse()
            metrics_data[jm.name] = {'events':[n.at for n in notifications]}
            metrics_data[jm.name]['data_label'] = jm.data_label
            metrics_data[jm.name]['metric_data'] = []
            for fn in jm.field_names.split(','):
                temp_data = {'field_name':fn}
                if fn == 'duration':
                    temp_data['data'] = [n.duration for n in notifications]
                elif not jm.client_supplied and len(jm.regex):
                    temp_data['data'] = []
                    for n in notifications:
                        temp_data['data'].append(re.search(jm.regex,n.log,re.DOTALL+re.MULTILINE).groupdict().get(fn,None))
                elif jm.client_supplied:
                    temp_data['data'] = []
                    for n in notifications:
                        try:
                            temp_data['data'].append(n.extra_info.get(field_name=fn).field_value)
                        except:
                            temp_data['data'].append('Null')
                metrics_data[jm.name]['metric_data'].append(temp_data)


        return render_to_response('job.html',{'job':job,'metrics':metrics_data},context_instance=RequestContext(request))


def job_group(request,job_group_slug=None):
    if job_group_slug:
        job_group = JobGroup.objects.get(slug=job_group_slug)
        return render_to_response('job_group.html',{'job_group':job_group},context_instance=RequestContext(request))
    else:
        job_groups = JobGroup.objects.all()
        return render_to_response('job_groups.html',{'job_groups':job_groups},context_instance=RequestContext(request))

