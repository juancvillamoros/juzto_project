from django.urls import path
from dashboard.views import DashboardView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

] 
