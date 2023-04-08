from django.shortcuts import render, redirect
from .forms import ReporteForm
from .models import Reporte
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def report_list(request):
    reportes = Reporte.objects.filter(user=request.user).order_by('-creado_en')
    return render(request, 'report_list.html', {'reportes': reportes})

@login_required
def report_bug(request):
    if request.method == 'POST':
        form = ReporteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('report_list')
    else:
        form = ReporteForm()
    return render(request, 'report_form.html', {'form': form})
