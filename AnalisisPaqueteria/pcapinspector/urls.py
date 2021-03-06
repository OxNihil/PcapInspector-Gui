from django.conf.urls import include, url
from pcapinspector import views
from maps import views as views2
from django.contrib.auth.views import LoginView

urlpatterns=[
	url(r'^$', views.index, name='index'),
	url(r'^upload/', views.upload, name='upload'),
	url(r'^register/', views.register_view, name='register'),
	url(r'^login/',  LoginView.as_view(template_name='signup.html'), name='login'),
	url(r'^maps/',views2.index, name='map'),
	url(r'^stats/', views.stats, name='stats'),
	url(r'^ipinfo/', views.ipinfo, name='ipinfo'),
	url(r'^report/',views.report, name='report'),
	url(r'^graph/', views.graph, name='graph'),
	url(r'^pcaps/',views.pcaps, name='pcaps'),
	url(r'^(?P<filename>[\w.]{0,256})/$',views.select_pcap, name='select'),
]
