from django.shortcuts import render
from django.http import HttpResponse
from django_cas_ng import views as baseviews
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return HttpResponse("Flipp Performance Tracking Optimizer 3000")
