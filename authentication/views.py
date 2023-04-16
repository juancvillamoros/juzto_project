from django.shortcuts import redirect
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def sign_out(request):
    logout(request)
    return redirect('home')
