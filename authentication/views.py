from django.shortcuts import redirect
from django.contrib.auth import logout
from django.shortcuts import render

# Create your views here.
def sign_out(request):
    logout(request)
    return redirect('home')
