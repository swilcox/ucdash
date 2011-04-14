from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.datetime_safe import datetime, date
from models import Job, JobGroup, Notification
from django.contrib.auth.decorators import login_required
import re


@login_required
def dashboard(request):
    job_groups = JobGroup.objects.all()
    jobs = Job.objects.all()
    return render_to_response('dashboard.html',{'jobs':jobs,'job_groups':job_groups},context_instance=RequestContext(request))


@login_required
def notification_detail(request,notification_id=None):
    if notification_id:
        notification = Notification.objects.get(id=notification_id)
    else:
        notification = None
    return render_to_response('notification_detail.html',{'notification':notification},context_instance=RequestContext(request))


@login_required
def job(request,job_slug=None,start_date=None,end_date=None,latest_count=10):
    #print request.META
    if job_slug:
        summary = None
        job = Job.objects.get(slug=job_slug)
        job_metrics = job.metrics.all()
        try:
            job.extra_display_fields = [df.strip() for df in job.config.display_extra_fields.split(',')]
            if len(job.config.multipart_field):
                if start_date is None and end_date is None:
                    start_date = date.today()
                    end_date = date.fromordinal(date.today().toordinal() + 1)

        except Exception, ex:
            print str(ex)
            job.extra_display_fields = ['log',]

        #this is where we decide how many and which notifications to display!!!!
        if start_date is not None and end_date is not None:
            notifications = job.notifications.filter(at__gte=start_date,at__lt=end_date)
        else:
            notifications = job.notifications.all()[:latest_count]

        notifications = [n for n in notifications]
        multipart = False
        multipart_field = None
        multipart_values = {}
        try:
            if len(job.config.multipart_field):
                multipart = True
                multipart_field = job.config.multipart_field
                for v in job.config.multipart_names.split(','):
                    multipart_values[v.strip()] = None
        except Exception, ex:
            pass

        for n in notifications:
            if multipart:
                try:
                    multipart_values[n.extra_info.get(field_name=multipart_field).field_value] = n.result
                except Exception, ex:
                    pass

            n.extra_fields = []
            for ef in job.extra_display_fields:
                if ef == 'log':
                    n.extra_fields.append('<PRE>' + n.log + '</PRE>')
                else:
                    try:
                        n.extra_fields.append(str(n.extra_info.get(field_name=ef).field_value))
                    except Exception, ex:
                        print ex
                        n.extra_fields.append('')
        if multipart:
            summary={}
            summary['total_parts'] = len(multipart_values)
            summary['good_results'] = sum(1 for v in multipart_values.values() if v is not None and v == 0)
            summary['bad_results'] = sum(1 for v in multipart_values.values() if v is not None and v != 0)
            summary['missing_results'] = sum(1 for v in multipart_values.values() if v is None)
        metrics_data = {}
        for jm in job_metrics:
            m_notifications = notifications[:]
            m_notifications.reverse()
            metrics_data[jm.name] = {'events':[n.at for n in m_notifications]}
            metrics_data[jm.name]['data_label'] = jm.data_label
            metrics_data[jm.name]['metric_data'] = []
            for fn in jm.field_names.split(','):
                fname = fn.strip()
                temp_data = {'field_name':fname}
                if fname == 'duration':
                    temp_data['data'] = [n.duration for n in m_notifications]
                elif len(jm.regex):
                    temp_data['data'] = []
                    for n in m_notifications:
                        try:
                            data_value = re.search(jm.regex,n.log,re.DOTALL+re.MULTILINE).groupdict().get(fname,'null')
                        except:
                            #todo: log the exception
                            data_value = 'null'
                        temp_data['data'].append(data_value)
                else:
                    temp_data['data'] = []
                    for n in m_notifications:
                        try:
                            temp_data['data'].append(n.extra_info.get(field_name=fname).field_value)
                        except:
                            temp_data['data'].append('null')
                metrics_data[jm.name]['metric_data'].append(temp_data)

        return render_to_response('job.html',{'job':job,'notifications':notifications,'metrics':metrics_data,'summary':summary,'host':request.get_host()},context_instance=RequestContext(request))


@login_required
def job_group(request,job_group_slug=None):
    if job_group_slug:
        job_group = JobGroup.objects.get(slug=job_group_slug)
        return render_to_response('job_group.html',{'job_group':job_group},context_instance=RequestContext(request))
    else:
        job_groups = JobGroup.objects.all()
        return render_to_response('job_groups.html',{'job_groups':job_groups},context_instance=RequestContext(request))

