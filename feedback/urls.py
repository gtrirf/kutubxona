from django.urls import path
from . import views

urlpatterns = [
    path('feedback/', views.feedback_view, name='feedback'),
    path('thank-you/', views.thank_you_view, name='thank_you'),
]
