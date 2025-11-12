from django.urls import path
from . import views

app_name = 'protips'

urlpatterns = [
	path('', views.index, name='index'),
	path('register/', views.register_view, name='register'),
	path('login/', views.login_view, name='login'),
	path('logout/', views.logout_view, name='logout'),
    path('tip/<int:tip_id>/vote/', views.tip_vote, name='tip_vote'),
	path('tip/<int:tip_id>/delete/', views.tip_delete, name='tip_delete'),
]
