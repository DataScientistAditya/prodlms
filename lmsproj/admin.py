from django.contrib import admin
from lmsproj.models import Account,Courses, Exam,Batch,Task,TaskSubmission,BatchCourseAssign


# Register your models here.
admin.site.register(Account)
admin.site.register(Courses)
admin.site.register(Batch)
admin.site.register(Exam)
admin.site.register(Task)
admin.site.register(TaskSubmission)
admin.site.register(BatchCourseAssign)
