from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import render

class DashboardView(TemplateView):
    template_name = 'dashboard/index.html'

def home(request):
    return HttpResponse(render(request, 'home/index.html'))
