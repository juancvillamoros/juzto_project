from django.contrib import admin
from django.urls import path, include
from authentication import views as auth_views
from dashboard import views as home_views
from dashboard.views import DashboardView
from capacitaciones import views as capacitaciones_views
from video_upload import views as video_views
from reportarbugs import views as bugs_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_views.home, name='home'), 
    path('accounts/', include('django.contrib.auth.urls')),
    path('sign_out/', auth_views.sign_out, name='sign_out'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('subir-video/', video_views.upload_video, name='upload_video'),
    path('lista_de_videos/', video_views.video_list, name='video_list'),
    path('capacitaciones/', capacitaciones_views.index, name='capacitaciones'),
    path('report/', bugs_views.report_bug, name='report_bug'),
    path('report_list/', bugs_views.report_list, name='report_list'),
]
