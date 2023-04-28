from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from user import views

urlpatterns = [
    path('', views.UserAPI.as_view()),
	path('jobs/', views.ScriptJobAPI.as_view()),
    path('login/', views.login),
]

urlpatterns = format_suffix_patterns(urlpatterns)