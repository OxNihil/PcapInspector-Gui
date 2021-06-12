from django.conf.urls import include, url
from pcapinspector import views
from maps import views as views2

urlpatterns=[
	url(r'^$', views.index, name='index'),
	url(r'^upload/', views.upload, name='upload'),
	url(r'^maps/',views2.index, name='map'),
]
