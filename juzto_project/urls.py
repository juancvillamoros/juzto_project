from django.contrib import admin
from django.urls import path, include
from authentication import views as auth_views
from dashboard import views as home_views
from capacitaciones import views as capacitaciones_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_views.home, name='home'), 
    path('accounts/', include('django.contrib.auth.urls')),
    path('sign_out/', auth_views.sign_out, name='sign_out'),
    path('dashboard/', include('dashboard.urls')),
    path('video_upload/', include('video_upload.urls')),
    path('video_list/', include('video_upload.urls', namespace='video_list')), 
    path('capacitaciones/', capacitaciones_views.index, name='capacitaciones'),
    path('reportar/', include('reportarbugs.urls')),
    path('listar_reportes/', include('reportarbugs.urls', namespace='reportarbugs')),
]
