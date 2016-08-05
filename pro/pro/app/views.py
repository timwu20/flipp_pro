from django.shortcuts import render
from django.http import HttpResponse
from django_cas_ng import views as baseviews
from django.views.decorators.csrf import csrf_exempt
from pro.app.models import Case, Employee, Coach
from django.views import generic

def index(request):
    if request.user.employee.coach:
        cases = Case.objects.filter(coach=request.user.employee)
    return render(request, 'index.html', {
        'employee': request.user.employee,
        'open_cases': cases, 
    })

def addTeam(request, u_id):
	coach = Coach.objects.get(user_id=u_id)
	added = False
	if not request.method == 'POST':
		employee_list = Employee.objects.all()
		employee_list = list(filter((lambda x: 
										not x in coach.employee_set.all() and x != coach.employee_ptr)
									, employee_list))
		return render(request, 'team.html', {
			'coach' : coach,
			'employee_list': employee_list,
			'added': added
		})
	new_employees = request.POST.getlist('employee')
	for employee in new_employees: 
		print(employee)
		coach.employee_set.add(Employee.objects.get(user_id=employee))
	coach.save()
	print(coach.employee_set.all())
	added = True
	return render(request, 'team.html', {
		'added': added
		})
		
def showEmployees(request, uid, option):
	coach = Coach.objects.get(user_id = uid)
	employee_list = Employee.objects.all()
	if option == "remove":
		employee_list = coach.employee_set.all()
	elif option == "add": 
		employee_list = list(filter((lambda x: 
										not x in coach.employee_set.all() and x != coach.employee_ptr), Employee.objects.all()))
	else:
		employee_list = Employee.objects.all()
	return render(request, 'employees.html', {
		'coach' : coach,
		'employee_list': employee_list,
		'option': option
	})

def editTeam(request, uid, option):
	selected = request.POST.getlist('employee')
	coach = Coach.objects.get(user_id = uid)
	if option == "add":
		for employee in selected: 
			coach.employee_set.add(Employee.objects.get(user_id=employee))
	else:
		for employee in selected:
			coach.employee_set.remove(Employee.objects.get(user_id=employee))
	coach.save()
	return render(request, 'employees.html', {
		'coach': coach,
		'employee_list': coach.employee_set.all(),
		'option': "all"
	})
	
	
