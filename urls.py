from django.conf.urls import url
from django.views.generic import RedirectView
from . import views

urlpatterns = [
	# welcome page
	url(r'^$', views.welcome, name='welcome'),
]