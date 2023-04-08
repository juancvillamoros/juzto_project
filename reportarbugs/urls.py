from django.urls import path
from . import views

app_name = 'reportarbugs'

urlpatterns = [
    path('listar_reportes/', views.report_list, name='report_list'),
    path('reportar/', views.report_bug, name='report_bug'),
]
