from django.shortcuts import render
from django.http import HttpResponse
from django_cas_ng import views as baseviews
from django.views.decorators.csrf import csrf_exempt
from pro.app.models import Case, Employee, Coach

def index(request):
    if request.user.employee.coach:
        cases = Case.objects.filter(coach=request.user.employee)
    return render(request, 'index.html', {
        'employee': request.user.employee,
        'open_cases': cases, 
    })

def addTeam(request, coach_id):
	coach = Coach.objects.get(pk=coach_id)
	added = false
	if not request.method == 'POST':
		employee_list = Employees.objects.all()
		employee_list = filter((lambda x: not x in coach.employees), employee_list)
		return render(request, 'team.html', {
			'employee_list': employee_list,
			'added': added
		})
	new_employees = request.POST.getlist('employee')
	for employee in new_employees: 
		print(employee)
		employee.coach = coach
		employee.save()
	coach.save()
	added = true
	return render(request, 'team.html', {
		'added': added
		})
		


	
