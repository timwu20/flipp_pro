from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	coach = models.ForeignKey('Coach', null=True, on_delete=models.CASCADE, related_name="employees")

	position = models.CharField(max_length=100)
	department = models.CharField(max_length=100)
	phone_number = models.CharField(max_length=10)

class Coach(Employee):

	employee_ptr = models.OneToOneField('Employee', related_name="%(app_label)s_%(class)s_related")

	def get_num_employees():
		return self.employees.count()


		
		



