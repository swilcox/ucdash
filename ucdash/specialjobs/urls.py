from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'specialjobs.views.special_dashboard'),
    (r'^job/(?P<job_slug>.*)/(?P<date_filter>.*)/$','specialjobs.views.special_job'),
    url(r'^job/(?P<job_slug>.*)/$','specialjobs.views.special_job',name='job-detail'),
    )
