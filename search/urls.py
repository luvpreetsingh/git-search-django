from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^', views.home , name='home'),
    url(r'^error$', views.error , name='error'),
    url(r'^(?P<username>\w+)', views.results , name='results'),
]
