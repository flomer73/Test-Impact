from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Templates
    url(r'^index', 'controllers.views.index', name='index'),
    url(r'^triangle/(?P<area>\d+)/(?P<tipo>\w+)/(?P<points>\w+)', 'controllers.views.getResponseTriangle', name='getResponseTriangle'),
    url(r'^square/(?P<area>\d+)/(?P<points>\w+)', 'controllers.views.getResponseSquare', name='getResponseSquare'),
    
)