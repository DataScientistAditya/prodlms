from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.conf import settings


# Create your models here.

# Custom User Model
class MyAccountManager(BaseUserManager):
    def create_user(self,email,username,password):
        if not email:
            raise ValueError("User must have a email")
        if not username:
            raise ValueError("User must have a Username")

        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self,email,username,password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email",max_length=100,unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined",auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login",auto_now_add=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_emailverified = models.BooleanField(default=False)
    phonenumber = models.CharField(max_length=13)
    firstname = models.CharField(max_length=50,default="N/A")
    lastname = models.CharField(max_length=100,default="N/A")
    isTeacher = models.BooleanField(default=False)
    isStudent = models.BooleanField(default=False)



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS= ['username']


    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self,perm,obj=None):
        return self.is_admin

    def has_module_perms(self,app_label):
        return True



User_Model = settings.AUTH_USER_MODEL

class Courses(models.Model):
    name = models.CharField(max_length=100)
    details = models.CharField(max_length=800)
    createdby = models.ForeignKey(User_Model, on_delete=models.CASCADE, related_name="course_creator")
    numberofmodules = models.IntegerField(default=1)
    datecreated = models.DateTimeField(auto_now_add=True)


    fistmodulename = models.CharField(max_length=20,default="n/a")
    fistmoduledays = models.IntegerField(default=1)
    firstmoduleteacher = models.ForeignKey(User_Model,default=None,on_delete=models.CASCADE,related_name="FirstModule_Teacher")

    secondmodulename = models.CharField(max_length=20,default="n/a")
    secondmoduledays = models.IntegerField(default=1)
    secondmoduleteacher = models.ForeignKey(User_Model,default=None,on_delete=models.CASCADE,related_name="SecondModule_Teacher")

    thirdmodulename = models.CharField(max_length=20,default="n/a")
    thirdmoduledays = models.IntegerField(default=1)
    thirdmoduleteacher = models.ForeignKey(User_Model,default=None,on_delete=models.CASCADE,related_name="ThirdModule_Teacher")

    fourthmodulename = models.CharField(max_length=20,default="n/a")
    fourthmoduledays = models.IntegerField(default=1)
    fourthmoduleteacher = models.ForeignKey(User_Model,default=None,on_delete=models.CASCADE ,related_name="FourthModule_Teacher")

    fifthmodulename = models.CharField(max_length=20,default="n/a")
    fifthmoduledays = models.IntegerField(default=1)
    fifthmoduleteacher = models.ForeignKey(User_Model,default=None,on_delete=models.CASCADE, related_name="FifthModule_Teacher")

    sixthmodulename = models.CharField(max_length=20,default="n/a")
    sixthmoduledays = models.IntegerField(default=1)
    sixthmoduleteacher = models.ForeignKey(User_Model,default=None,on_delete=models.CASCADE,related_name="SixthModule_Teacher")

    seventhmodulename = models.CharField(max_length=20, default="n/a")
    seventhmoduledays = models.IntegerField(default=1)
    seventhmoduleteacher = models.ForeignKey(User_Model,default=None, on_delete=models.CASCADE,related_name="SeventhModule_Teacher")



class Batch(models.Model):
    name = models.CharField(max_length=100)
    details = models.CharField(max_length=800)
    startdate = models.DateTimeField()
    enddate = models.DateTimeField()
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name="coursrealtedtobatch")
    modulename = models.CharField(max_length=20)
    isActive = models.BooleanField(default=False)



    


class Exam(models.Model):
    name = models.CharField(max_length=100)
    details = models.CharField(max_length=800)
    examdate = models.DateTimeField()
    duration = models.IntegerField(default=3)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE,related_name="exambatch")
    course = models.ForeignKey(Courses, on_delete=models.CASCADE,related_name="examcourse")
    datecreated = models.DateTimeField(auto_now_add=True, null=True)

    firstquestion = models.CharField(max_length=800, default="n/a")
    firstqsnoptionone = models.CharField(max_length=200,default="n/a")
    firstqsnoptiontwo = models.CharField(max_length=200,default="n/a")
    firstqsnoptionthree = models.CharField(max_length=200,default="n/a")
    firstqsnoptionfour = models.CharField(max_length=200,default="n/a")
    firstqsnAnswer = models.CharField(max_length=200,default="n/a")


    secondquestion = models.CharField(max_length=800,default="n/a")
    secondqsnoptionone = models.CharField(max_length=200,default="n/a")
    secondqsnoptiontwo = models.CharField(max_length=200,default="n/a")
    secondqsnoptionthree = models.CharField(max_length=200,default="n/a")
    secondqsnoptionfour = models.CharField(max_length=200,default="n/a")
    secondqsnAnswer = models.CharField(max_length=200,default="n/a")


    thirdquestion = models.CharField(max_length=800,default="n/a")
    thirdqsnoptionone = models.CharField(max_length=200,default="n/a")
    thirdqsnoptiontwo = models.CharField(max_length=200,default="n/a")
    thirdqsnoptionthree = models.CharField(max_length=200,default="n/a")
    thirdqsnoptionfour = models.CharField(max_length=200,default="n/a")
    thirdqsnAnswer = models.CharField(max_length=200,default="n/a")


    fourthquestion = models.CharField(max_length=800,default="n/a")
    fourthqsnoptionone = models.CharField(max_length=200,default="n/a")
    fourthqsnoptiontwo = models.CharField(max_length=200,default="n/a")
    fourthqsnoptionthree = models.CharField(max_length=200,default="n/a")
    fourthqsnoptionfour = models.CharField(max_length=200,default="n/a")
    fourthqsnAnswer = models.CharField(max_length=200,default="n/a")


    fifthquestion = models.CharField(max_length=800,default="n/a")
    fifthqsnoptionone = models.CharField(max_length=200,default="n/a")
    fifthqsnoptiontwo = models.CharField(max_length=200,default="n/a")
    fifthqsnoptionthree = models.CharField(max_length=200,default="n/a")
    fifthqsnoptionfour = models.CharField(max_length=200,default="n/a")
    fifthqsnAnswer = models.CharField(max_length=200,default="n/a")



    


class Task(models.Model):
    name = models.CharField(max_length=100)
    details = models.CharField(max_length=800)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name="taskbatch")
    startdate = models.DateTimeField()
    enddate = models.DateTimeField()
    task = models.CharField(max_length=1000)
    isActive = models.BooleanField(default=True)
    createdby = models.ForeignKey(User_Model,on_delete=models.CASCADE,null=True, related_name="taskcreateduser")
    date_created = models.DateTimeField(auto_now_add=True,null=True)





class BatchCourseAssign(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name="assigingusertobatch")
    course = models.ForeignKey(Courses, on_delete=models.CASCADE,null=True, related_name="Assign_Course")
    activeModule = models.CharField(max_length=20,default="n/a")
    user = models.ForeignKey(User_Model,on_delete=models.CASCADE)



class TaskSubmission(models.Model):
    student = models.ForeignKey(User_Model,on_delete=models.CASCADE, related_name="tasksubmittedstudent")
    taskanswer = models.CharField(max_length=1000)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="tasktobesubmited")
    grade = models.IntegerField(default=0)
    dateofsubmission = models.DateTimeField(auto_now_add=True, null=True)


class ExamSubmit(models.Model):
    student = models.ForeignKey(User_Model,on_delete=models.CASCADE, related_name="examubmittedstudent")
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    firstanswer = models.CharField(max_length=100)
    secondanswer = models.CharField(max_length=100)
    thirdasnswer = models.CharField(max_length=100)
    fourthanswer = models.CharField(max_length=100)
    fifthanswer = models.CharField(max_length=100)
    grade = models.IntegerField(default=0)
    dateofsubmission = models.DateTimeField(auto_now_add=True, null=True)






    