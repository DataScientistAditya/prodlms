from rest_framework.views import APIView
from lmsproj.models import Account, Batch, Courses, ExamSubmit, Task,Exam,BatchCourseAssign, TaskSubmission
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

#Must Update student and Teacher Assignment each time if it's there to be updated
class AllUsers(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        Data = Account.objects.all().values("id","email","firstname","lastname","phonenumber","isTeacher","isStudent","password")
        print(Data)
        for i in Data:
            try:
                BatchId = BatchCourseAssign.objects.filter(user = i["id"]).values("batch")
                Course_Id = BatchCourseAssign.objects.filter(user = i["id"]).values("course")
                i["batch"] = BatchId
                i["course"] = Course_Id
            except:
                i["batch"] = "None"
                i["course"] = "None"
        return Response({"msg":"Data fetched", "data":Data, "status":status.HTTP_200_OK})


class AllCourses(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        Data = Courses.objects.all().values("id","name","createdby","numberofmodules","datecreated")
        ListofCourseData = []
        for i in Data:
            BatchObj = Batch.objects.filter(course = i["id"]).values("name")
            CourseData = {
                "id":i["id"],
                "name":i["name"],
                "createdby":Account.objects.get(id = int(i["createdby"])).username,
                "numberofmodules":i["numberofmodules"],
                "datecreated":i["datecreated"],
                "numberofbatch":len(BatchObj)
            }
            ListofCourseData.append(CourseData)
        return Response({"msg":"Data fetched", "data":ListofCourseData, "status":status.HTTP_200_OK})

class AllBatch(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        Data = Batch.objects.all().values("id","name","course","startdate","enddate","modulename")   
        return Response({"msg":"Data fetched", "data":Data, "status":status.HTTP_200_OK})

class AllTask(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        Data = Task.objects.all().values("id","name","details","startdate","enddate","task","isActive","batch")
        return Response({"msg":"Data fetched", "data":Data, "status":status.HTTP_200_OK})

class AllExam(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        ExamDetails = Exam.objects.all().values("name","details","examdate","duration","course",
                                                "firstquestion","firstqsnoptionone","firstqsnoptiontwo","firstqsnoptionthree","firstqsnoptionfour","firstqsnAnswer",
                                                "secondquestion","secondqsnoptionone","secondqsnoptiontwo","secondqsnoptionthree","secondqsnoptionfour","secondqsnAnswer",
                                                "thirdquestion","thirdqsnoptionone","thirdqsnoptiontwo","thirdqsnoptionthree","thirdqsnoptionfour","thirdqsnAnswer",
                                                "fourthquestion","fourthqsnoptionone","fourthqsnoptiontwo","fourthqsnoptionthree","fourthqsnoptionfour","fourthqsnAnswer",
                                                "fifthquestion","fifthqsnoptionone","fifthqsnoptiontwo","fifthqsnoptionthree","fifthqsnoptionfour","fifthqsnAnswer").order_by("-datecreated")
        return Response({"msg":"Data fetched", "data":ExamDetails, "status":status.HTTP_200_OK})


class AllAssignments(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        AllAssignObj = BatchCourseAssign.objects.all().values("batch","course","activeModule","user")
        return Response({"msg":"Data fetched", "data":AllAssignObj, "status":status.HTTP_200_OK})

class AllSubmittedTask(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        Listof_SubmittedTask= []
        TaskObj = TaskSubmission.objects.all().values("id","student","taskanswer","task","dateofsubmission").order_by("-dateofsubmission")
        for i in TaskObj:
            StudentObj = TaskSubmission.objects.select_related("student").get(id = i["id"]).student
            TaskObj = TaskSubmission.objects.select_related("task").get(id = i["id"]).task
            Data = {
                "id":i["id"],
                "student_email":StudentObj.email,
                "student_username":StudentObj.username,
                "answer": i["taskanswer"],
                "taskname": TaskObj.name,
                "submitdate":i["dateofsubmission"]
            }
            Listof_SubmittedTask.append(Data)
        return Response({"msg":"Data fetched", "data":Listof_SubmittedTask, "status":status.HTTP_200_OK})

class AllSubmittedExam(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        ListofSubmittedExam = []
        ExamObjs = ExamSubmit.objects.all().values("id","student","exam","firstanswer","secondanswer","thirdasnswer","fourthanswer","fifthanswer")
        for i in ExamObjs:
            StudentObj = ExamSubmit.objects.select_related("student").get(id = i["id"]).student
            ExamObj = ExamSubmit.objects.select_related("exam").get(id = i["id"]).exam
            Data={
                "id":i["id"],
                "student_email": StudentObj.email,
                "student_username": StudentObj.username,
                "exam_name": ExamObj.name,
                "firstqsn": ExamObj.firstquestion,
                "firstqsnrightanswer": ExamObj.firstqsnAnswer,
                "firstqsnstudentanswer": i["firstanswer"],
                "sencondqsn": ExamObj.secondquestion,
                "secondqsnrightanswer": ExamObj.secondqsnAnswer,
                "secondqsnstudentanswer": i["secondanswer"],
                "thirdqsn": ExamObj.thirdquestion,
                "thirdqsnrightanswer": ExamObj.thirdqsnAnswer,
                "thirdqsnstudentanswer": i["thirdasnswer"],
                "fourthqsn": ExamObj.fourthquestion,
                "fourthqsnrightanswer": ExamObj.fourthqsnAnswer,
                "fourthqsnstudentanswer": i["fourthanswer"],
                "fifthqsn": ExamObj.fifthquestion, 
                "fifthqsnrightanswer": ExamObj.fifthqsnAnswer,
                "fifthqsnstudentanswer": i["fifthanswer"],
            }
            ListofSubmittedExam.append(Data)
        return Response({"msg":"Data fetched", "data":ListofSubmittedExam, "status":status.HTTP_200_OK})
        


        