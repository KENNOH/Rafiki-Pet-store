from django.conf.urls import url,include
from . import views




urlpatterns = [
	url(r'^dashboard/pets/', views.check, name='check'),
	url(r'^dashboard/transactions/', views.trans, name='trans'),
	url(r'^dashboard/start/', views.start, name='start'),
	url(r'^dashboard/edit_pets/(?P<urlhash>[0-9A-Za-z_\-]+)/$',views.edit_pets, name='edit_pets'),
	url(r'^generate_pdf/', views.generate_pdf, name='generate_pdf'),
	url(r'^dashboard/profile/', views.update_profile, name='update_profile'),
	url(r'^dashboard/process_payment/(?P<urlhash>[0-9A-Za-z_\-]+)/$',views.process_payment, name='process_payment'),
	url(r'^dashboard/add_service/', views.add_service, name='add_service'),
	url(r'^dashboard/expand_pet/(?P<pk>[0-9]+)$',views.expand_pet, name='expand_pet'),
	url(r'^dashboard/',views.dashboard,name='dashboard'),
	url(r'^process_lnms/$', views.process_lnm, name='process_lnm'),
]
