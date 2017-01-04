from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.captcha, name = 'captcha'),
    url(r'^demo', views.demo, name = 'demo')
]
