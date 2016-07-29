from django.shortcuts import render
from django.http import HttpResponse
from django_cas_ng import views as baseviews
from django.views.decorators.csrf import csrf_exempt
from pro.app.models import Case

def index(request):
    if request.user.employee.coach:
        cases = Case.objects.filter(coach=request.user.employee)
    return render(request, 'index.html', {
        'employee': request.user.employee,
        'open_cases': cases, 
    })
