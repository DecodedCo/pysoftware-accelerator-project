from django.urls import path
from . import views

urlpatterns = [
    path('test-django-api/', views.test_django_api),
    path('submit-data/', views.test_submit_data),
    path('request-data', views.test_request_data),
]
