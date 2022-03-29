from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "index.html")

def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, 'about.html')
    
# FOR TESTING ONLY
def base_file(request):
    return render(request, 'base_file.html')

