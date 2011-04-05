from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
      (r'^$', 'jobs.views.dashboard'),
      (r'^special/', include('specialjobs.urls',namespace='specialjobs')),
      (r'^notification-detail/(?P<notification_id>.*)/$','jobs.views.notification_detail'),
      (r'^job/(?P<job_slug>.*)/$','jobs.views.job'),
      (r'^job-group/(?P<job_group_slug>.*)/$','jobs.views.job_group'),
      (r'^api/', include('ucdash.api.urls',namespace='api')),
      url(r'^accounts/login/$', 'django.contrib.auth.views.login'),

    # Example:
    # (r'^ucdash/', include('ucdash.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
