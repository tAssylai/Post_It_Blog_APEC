from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'post_it/index.html')

def newpost(request):
    return render(request, 'post_it/newpost.html')