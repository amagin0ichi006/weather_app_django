from django.urls import path
from . import views

urlpatterns = [
    path('my-home/', views.index, name='my-home'),
]