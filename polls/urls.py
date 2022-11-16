from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, kwargs=None, name='index'),
]
