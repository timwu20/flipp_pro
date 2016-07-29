from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals

class Employee(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	coach = models.ForeignKey('Coach', null=True, on_delete=models.CASCADE, related_name="employees")

	position = models.CharField(max_length=100)
	department = models.CharField(max_length=100)
	phone_number = models.CharField(max_length=10)

	def __str__(self):
		return '%s' % self.user

def create_employee(sender, instance, created, **kwargs):
    Employee.objects.get_or_create(user=instance)

signals.post_save.connect(create_employee, sender=User, weak=False, dispatch_uid='create_employee')

class Approver(Employee):
	employee = models.OneToOneField(Employee, related_name="%(app_label)s_%(class)s_related")

	def __str__(self):
		return self.employee

class ApproverCoach(models.Model):
	approver = models.ForeignKey(Approver, on_delete=models.CASCADE)
	coach = models.ForeignKey('Coach', on_delete=models.CASCADE)
	sequence_order = models.IntegerField(default=0)

	def next_sequence_order(self):
		#not incrementing cause we can use 0 index
		return ApproverCoach.objects.filter(approver=self.approver, coach=self.coach).count()


class Coach(Employee):
	approvers = models.ManyToManyField(Approver, through=ApproverCoach, related_name='coaches')
	employee = models.OneToOneField(Employee, related_name="%(app_label)s_%(class)s_related")

	def get_num_employees():
		return self.employees.count()

	def __str__(self):
		return self.employee.user

	class Meta:
		verbose_name_plural = 'coaches'

class BaseForm(models.Model):
	case = models.ForeignKey('Case')
	submitted = models.BooleanField(default=False)
	submitted_date = models.DateTimeField(null=True, default=None)

	class Meta:
		abstract = True

class SelfEvaluation(BaseForm):
	pass

class PerformanceReview(BaseForm):
	pass

class Feedback360(BaseForm):
	provider = models.ForeignKey(Employee)

class CaseStatus(models.Model):
	status = models.CharField(max_length=100, blank=False, null=False)

class Case(models.Model):
	#people
	employee = models.ForeignKey(Employee)
	coach = models.ForeignKey(Coach, related_name='cases')

	#forms
	self_evaluation_form = models.OneToOneField(SelfEvaluation, related_name='cases')
	performance_review = models.OneToOneField(PerformanceReview, related_name='cases')

	feedback_360_forms = models.ForeignKey(Feedback360, related_name='cases')

	#status
	status = models.ForeignKey(CaseStatus)
