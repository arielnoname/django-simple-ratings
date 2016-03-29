from __future__ import absolute_import
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^create/$', views.create, name='rating_create'),
]
