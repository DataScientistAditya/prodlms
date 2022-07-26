from rest_framework_simplejwt.tokens import RefreshToken
from lmsproj.models import Account,BatchCourseAssign,TaskSubmission,Task,Exam
from django.contrib.auth.hashers import check_password

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def ValidateUser(Email=None, Password = None):
    try:
        UserPass = Account.objects.filter(email = Email).values("password")[0]["password"]
        isPassCheck = check_password(Password, UserPass)
        if isPassCheck:
            Account.objects.filter(email=Email).update(is_active =True)
            UserObj = Account.objects.get(email = Email)
            return UserObj
    except:
        return None


def TeacherObjs(data):
    # print(data)
    try: 
        FirstTeacher = Account.objects.get(id = int(data["firstmoduleteacher"]))
    except:
        FirstTeacher = None

    try:
        SecondTeacher = Account.objects.get(id = int(data["secondmoduleteacher"]))
    except:
        SecondTeacher = None

    try:
        ThirdTeacher = Account.objects.get(id = int(data["thirdmoduleteacher"]))
    except:
        ThirdTeacher = None

    try:
        FourthTeacher = Account.objects.get(id = int(data["fourthmoduleteacher"]))
    except:
        FourthTeacher = None

    try:
        FifthTeacher = Account.objects.get(id = int(data["fifthmoduleteacher"]))
    except:
        FifthTeacher = None
    
    try:
        SixthTeacher = Account.objects.get(id = int(data["sixthmoduleteacher"]))
    except:
        SixthTeacher = None
    
    try:
        SeventhTeacher = Account.objects.get(id = int(data["seventhmoduleteacher"]))
    except:
        SeventhTeacher = None

    return FirstTeacher, SecondTeacher, ThirdTeacher,FourthTeacher,FifthTeacher,SixthTeacher,SeventhTeacher


def GetCompletedandPendingTask(studentid):
    
    Batch_Id = BatchCourseAssign.objects.filter(user = studentid).values("batch")[0]["batch"]
    QuarySet = Task.objects.all().filter(batch = Batch_Id).values("id","name","details","startdate","enddate","task","isActive")
    Submitted_Task_List = []
    Pending_Task_List = []

    for i in QuarySet:
        try:
            Student_id = TaskSubmission.objects.filter(task = i["id"]).values("student")[0]["student"]
            if Student_id == studentid:
                Submitted_Task_List.append(i)
        except:
            Pending_Task_List.append(i)
    

    return Submitted_Task_List, Pending_Task_List





def GetProfileData(userid):
    
    UserObj = BatchCourseAssign.objects.select_related("batch").get(user=userid).user
    CourseObj = BatchCourseAssign.objects.select_related("course").get(user=userid).course
    BatchObj = BatchCourseAssign.objects.select_related("batch").get(user=userid).batch

    ObjectList = [
        {
            "name": UserObj.username,
            "email": UserObj.email,
            "phonenumber": UserObj.phonenumber,
            "datejoined": UserObj.date_joined,
            "course":CourseObj.name,
            "batch":BatchObj.name,
            "startdate": BatchObj.startdate,
            "enddate": BatchObj.enddate,
            "module": BatchObj.modulename,
        }
    ]

    return ObjectList




def GetEventsData(isAdmin =False, userid=None):
    List = []
    List_of_Task = []

    if len(List)>0:
        List.clear()
    if len(List_of_Task)>0:
        List_of_Task.clear()

    if isAdmin:
        TaskData = Task.objects.all().values("name","startdate").order_by("-date_created")
        return TaskData
    else:
        obj = BatchCourseAssign.objects.select_related("batch").filter(user = userid)
        
        if obj != None:
            for i in obj:
                if i.batch_id not in List:
                    List.append(i.batch_id)
                    TaskDetails = Task.objects.filter(batch = i.batch_id ).values("name","startdate").order_by("-date_created")
                    List_of_Task.append(TaskDetails)
        
            return List_of_Task


def GetExamData(userid = None):
    List = []
    List_of_Exam = []
    if len(List)>0:
        List.clear()
    if len(List_of_Exam)>0:
        List_of_Exam.clear()

    if userid != None:
        try:
            obj = BatchCourseAssign.objects.select_related("batch").filter(user = userid)
            # print(obj)
            for i in obj:
                if i.batch_id not in List:
                    List.append(i.batch_id)
                    print(List)
                    ExamDetails = Exam.objects.filter(batch = i.batch_id ).values("name","details","examdate","duration","course",
                                                                                    "firstquestion","firstqsnoptionone","firstqsnoptiontwo","firstqsnoptionthree","firstqsnoptionfour","firstqsnAnswer",
                                                                                    "secondquestion","secondqsnoptionone","secondqsnoptiontwo","secondqsnoptionthree","secondqsnoptionfour","secondqsnAnswer",
                                                                                    "thirdquestion","thirdqsnoptionone","thirdqsnoptiontwo","thirdqsnoptionthree","thirdqsnoptionfour","thirdqsnAnswer",
                                                                                    "fourthquestion","fourthqsnoptionone","fourthqsnoptiontwo","fourthqsnoptionthree","fourthqsnoptionfour","fourthqsnAnswer",
                                                                                    "fifthquestion","fifthqsnoptionone","fifthqsnoptiontwo","fifthqsnoptionthree","fifthqsnoptionfour","fifthqsnAnswer").order_by("-examdate")
                    List_of_Exam.append(ExamDetails)
            return List_of_Exam
        except:
            return None
    else:
        return None


                



        


        
                
        


            


        



