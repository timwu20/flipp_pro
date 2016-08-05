from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals

class Employee(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	boss = models.ForeignKey('Coach', blank=True, null=True, on_delete=models.CASCADE)

	position = models.CharField(max_length=100, blank=True, null=True)
	department = models.CharField(max_length=100, blank=True, null=True)
	phone_number = models.CharField(max_length=10, blank=True, null=True)

	#def __str__(self):
	#	return '%s %s' % (self.user.first_name, self.user.last_name)

	def create_coach(self):
		c = Coach(employee_ptr_id = self.pk)
		c.__dict__.update(self.__dict__)
		c.save()
		return c

	# Simply doing .delete() deletes the employee as well
	def delete_coach(self):
		coach_ptr = DelCoach.objects.get(pk=self.pk)
		coach_ptr.delete()
		return self

def create_employee(sender, instance, created, **kwargs):
    Employee.objects.get_or_create(user=instance)

signals.post_save.connect(create_employee, sender=User, weak=False, dispatch_uid='create_employee')

class Approver(Employee):
	pass
	#def __str__(self):
	#	return self.employee_ptr.__str__()

class ApproverCoach(models.Model):
	approver = models.ForeignKey(Approver, on_delete=models.CASCADE)
	coach = models.ForeignKey('Coach', on_delete=models.CASCADE)

	def next_sequence_order(self):
		#not incrementing cause we can use 0 index
		return ApproverCoach.objects.filter(coach=self.coach).count()

	sequence_order = models.IntegerField(default=next_sequence_order)

	#add default ordering to this model
	#class Meta:
	#	ordering = ['sequence_order']

class Coach(Employee):
	approvers = models.ManyToManyField(Approver, through=ApproverCoach, related_name='coaches')
	#employee_ptr = models.OneToOneField('Employee', parent_link=True, related_name="%(app_label)s_%(class)s_related")

	def get_num_employees():
		return self.employee_set.count()

	#def __str__(self):
		#	return self.employee_ptr.__str__()

	class Meta:
		verbose_name_plural = 'coaches'

# So you can unmake an employee a coach
class DelCoach(models.Model):
	employee_ptr = models.PositiveIntegerField(db_column="employee_ptr_id", primary_key=True)
	class Meta:
		app_label = Coach._meta.app_label
		db_table = Coach._meta.db_table
		managed = False
	
class BaseForm(models.Model):
	submitted = models.BooleanField(default=False)
	submitted_date = models.DateTimeField(blank=True, null=True, default=None)

	#add created
	class Meta:
		abstract = True

class SelfEvaluation(BaseForm):
	pass

class PerformanceReview(BaseForm):
	pass

class Feedback360(BaseForm):
	provider = models.ForeignKey(Employee)

class CaseStatus(models.Model):
	#look into django fixtures, in progress, submitted, rejected
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
