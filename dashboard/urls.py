from django.conf.urls import url,include
from . import views


urlpatterns = [
	url(r'^dashboard/pets/', views.check, name='check'),
	url(r'^dashboard/transactions/', views.trans, name='trans'),
	url(r'^dashboard/start/', views.start, name='start'),
	url(r'^dashboard/expand_pet/(?P<pk>[0-9]+)$',views.expand_pet, name='expand_pet'),
	url(r'^dashboard/',views.dashboard,name='dashboard'),
]
