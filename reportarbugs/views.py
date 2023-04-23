from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from .forms import ReporteForm
from .models import Reporte


@login_required
@csrf_protect
@csrf_exempt
def report_bug(request):
    if request.method == 'POST':
        form = ReporteForm(request.POST, request.FILES)
        if form.is_valid():
            reporte = form.save(commit=False)
            reporte.user = request.user
            reporte.save()
            return redirect('report_list')
    else:
        form = ReporteForm()
    return render(request, 'report_form.html', {'form': form})


@login_required
def report_list(request):
    reportes = Reporte.objects.filter(user=request.user).order_by('-creado_en')
    return render(request, 'report_list.html', {'reportes': reportes})



