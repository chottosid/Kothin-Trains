from django.shortcuts import render

# Create your views here.
def login(request):
    dict={}
    return render(request, "login.html", context=dict)

def homepage(request):
    dict={}
    return render(request, "search.html", context=dict)
