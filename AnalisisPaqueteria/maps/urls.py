from django.conf.urls import include, url
from maps import views

urlpatterns=[
	url(r'^$', views.index, name='index'),
]
