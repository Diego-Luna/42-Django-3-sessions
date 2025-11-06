from django.urls import path
from . import views

app_name = 'protips'

urlpatterns = [
	path('', views.index, name='index'),
]
