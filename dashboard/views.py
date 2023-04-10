from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

class DashboardView(TemplateView):
    template_name = 'dashboard/index.html'

@login_required
def dashboard(request):
    return DashboardView.as_view()(request)

def home(request):
    return HttpResponse(render(request, 'home/index.html'))
