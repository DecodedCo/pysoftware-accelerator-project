from django.urls import path
from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
    path('home/', TemplateView.as_view(template_name='home.html'), name='home'),
    path('results/', TemplateView.as_view(template_name='result.html'), name='result'),
]

