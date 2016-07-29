from django.contrib import admin
from pro.app.models import Employee, Approver, Coach, SelfEvaluation, PerformanceReview, Feedback360, CaseStatus, Case
# Register your models here.
admin.site.register(Employee)
admin.site.register(Approver)
admin.site.register(Coach)
admin.site.register(SelfEvaluation)
admin.site.register(PerformanceReview)
admin.site.register(Feedback360)
admin.site.register(CaseStatus)
admin.site.register(Case)
