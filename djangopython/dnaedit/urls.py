from django.conf.urls import patterns, url
from dnaedit import views

'''
    urls for the website are located here. Adding a url requires you to fill out the method url.
    
    Example: url(r'^<name of level>/$, <method associated to the extension for view>, name=<name of url>)
'''
urlpatterns = patterns('',
                       
    url(r'^upload/$', views.uploadFile, name='upload'),
    url(r'^ajaxTest/$', views.getDNAInformation, name='dnaInfo'),
    url(r'^ajaxDemo/$', views.fileSelectionAjax, name='ajaxFiles'),
    url(r'^ajaxDisplay/$', views.ajaxShowFiles, name='ajaxDisplay'),
    url(r'^get/labs/$', views.sendLabs, name='getLabs'),
    url(r'^get/files/$', views.sendFiles, name='getFiles'),
    url(r'^get/sequences/$', views.sendFileSequences, name='getSequences'),
    url(r'^upload/file/$', views.uploadLabFile, name='uploadLabFile'),
    url(r'^get/align/$',views.getAlignedSequences,name='align'),
    url(r'^get/distancematrix/$',views.getDistanceMatrix,name='distanceMatrix'),
    url(r'^get/rnatodna/$',views.getDNAFromRNA,name='rnatodna'),
    url(r'^get/dotmatrix/$',views.getDotMatrix,name='dotMatrix'),
    url(r'^get/inversedna/$',views.getInverseDNA,name='inverseDna'),
    url(r'^get/dnatoprotein/',views.getProteinFromDNA,name='dnatoprotein'),
    url(r'^get/rnatoprotein/$',views.getProteinFromRNA,name='rnatoprotein'),
    url(r'^get/dnatorna/$',views.getRNAFromDNA,name='dnatorna'),
    url(r'^get/topology/$',views.getTopologyFilePath,name='topologyFile'),
    url(r'^get/topology/string/$',views.getTopologyTreeString,name='topologyString'),
    url(r'^get/dotmatrix/string/$',views.getDistanceMatrixString,name='dotMatrixString'),
    url(r'^get/blaze/$',views.getBlazeReport,name='blaze')
    
)
