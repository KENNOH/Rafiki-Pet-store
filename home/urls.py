from django.conf.urls import url,include
from . import views

urlpatterns = [
    url(r'^$', views.site, name='site'), 
    url(r'^pets_display/', views.pets_display, name='pets_display'),
    url(r'^services_display/', views.services_display, name='services_display'),
    url(r'^make_review/(?P<urlhash>[0-9A-Za-z_\-]+)/$',views.make_review, name='make_review'),
    url(r'^pet_expand/(?P<urlhash>[0-9A-Za-z_\-]+)/$',views.pets_expand, name='pets_expand'),
    url(r'^sort/(?P<name>[\w.@+-]+)', views.sort, name='sort'),
]
