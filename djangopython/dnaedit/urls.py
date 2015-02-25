from django.conf.urls import patterns, url
from dnaedit import views
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'djangopython.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.index, name='index'),
    url(r'^lab/(?P<lab_id>\d+)/$', views.labSelection, name='labSelect'),
    url(r'^species/$', views.species, name='species'),
    url(r'^aligned/$', views.alignOutput, name='aligned'),
    url(r'^upload/$', views.uploadFile, name='upload'),
    url(r'^dna/$', views.fileHandler, name='dna'),
    
)
