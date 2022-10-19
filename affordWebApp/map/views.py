from django.http import JsonResponse
from django.shortcuts import render
from . import models

# Create your views here.
def index(request):
    return render(request, "index.html")

def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, 'about.html')
    
def state_pop(request):
    data = models.statePop.objects.all().values()
    return JsonResponse(list(data), safe=False)

# FOR TESTING ONLY
def base_file(request):
    return render(request, 'base_file.html')

