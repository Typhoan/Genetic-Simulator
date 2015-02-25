from django.conf.urls import patterns, url
from dnaedit import views

'''
    urls for the website are located here. Adding a url requires you to fill out the method url.
    
    Example: url(r'^<name of level>/$, <method associated to the extension for view>, name=<name of url>)
'''
urlpatterns = patterns('',

    url(r'^$', views.index, name='index'),
    url(r'^lab/(?P<lab_id>\d+)/$', views.labSelection, name='labSelect'),
    url(r'^species/$', views.species, name='species'),
    url(r'^aligned/$', views.alignOutput, name='aligned'),
    url(r'^upload/$', views.uploadFile, name='upload'),
    url(r'^dna/$', views.fileSparse, name='dna'),
    
)
