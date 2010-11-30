from django.conf.urls.defaults import *
from piston.resource import Resource
from handlers import JobNotificationHandler

jobnotification_handler = Resource(JobNotificationHandler)

urlpatterns = patterns('',
   url(r'^notify/(?P<job_slug>[^/]+)/', jobnotification_handler),
)