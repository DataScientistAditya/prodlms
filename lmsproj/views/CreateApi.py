from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from lmsproj.createserilizers import CreateCourseSerializer,CreateBatchSerializer, CreateTaskSerializer,CreateExamSerializer
from rest_framework.permissions import IsAuthenticated
from lmsproj.models import Account,Courses,Batch, Exam, Task
from lmsproj.utils import TeacherObjs
import datetime



class CreateCourse(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:
            Serializer = CreateCourseSerializer(data= request.data)
            if Serializer.is_valid():
                UserObject = Account.objects.get(email = request.user)
                FirstTeacher, SecondTeacher, ThirdTeacher,FourthTeacher,FifthTeacher,SixthTeacher,SeventhTeacher = TeacherObjs(data=request.data)
                validated_data = request.data

                Courses.objects.create(name = validated_data["name"],createdby = UserObject ,details =validated_data["details"] , numberofmodules = validated_data["numberofmodules"],
                        fistmodulename = validated_data["fistmodulename"], fistmoduledays= int(validated_data["fistmoduledays"]),firstmoduleteacher = FirstTeacher ,
                        secondmodulename = validated_data["secondmodulename"], secondmoduledays = int(validated_data["secondmoduledays"]),secondmoduleteacher = SecondTeacher,
                        thirdmodulename = validated_data["thirdmodulename"],thirdmoduledays = int(validated_data["thirdmoduledays"]),thirdmoduleteacher = ThirdTeacher ,
                        fourthmodulename =  validated_data["fourthmodulename"],fourthmoduledays = int(validated_data["fourthmoduledays"]),fourthmoduleteacher = FourthTeacher,
                        fifthmodulename = validated_data["fifthmodulename"], fifthmoduledays = int(validated_data["fifthmoduledays"]), fifthmoduleteacher = FifthTeacher,
                        sixthmodulename = validated_data["sixthmodulename"], sixthmoduledays = int(validated_data["sixthmoduledays"]), sixthmoduleteacher = SixthTeacher,
                        seventhmodulename = validated_data["seventhmodulename"], seventhmoduledays = int(validated_data["seventhmoduledays"]), seventhmoduleteacher = SeventhTeacher)

                return Response({"msg":"Course Created", "status":status.HTTP_201_CREATED})

            return Response({"msg":"Course not Created","error":"Serializer is not Valid", "status":status.HTTP_401_UNAUTHORIZED})
        except Exception as e:
            return Response({"msg":"Course not Created","error":e, "status":status.HTTP_417_EXPECTATION_FAILED})



class CreateBatch(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        Serializer = CreateBatchSerializer(data=request.data)
        # print(request.data)
        if Serializer.is_valid(raise_exception=True):
            try:
                CourseObj = Courses.objects.get(id = int(request.data["course"]))
                StartDate = datetime.datetime.strptime(request.data["startdate"],"%Y-%m-%d %H:%M")
                EndDate =   datetime.datetime.strptime(request.data["enddate"],"%Y-%m-%d %H:%M")
                validated_data = request.data
                if validated_data["isActive"] == 1:
                    Active = True
                else:
                    Active = False

                ModuleName = Courses.objects.filter(id = int(validated_data["course"])).values(validated_data["modulename"])
                
                Batch.objects.create(name = validated_data["name"] , details = validated_data["details"],
                                    startdate = StartDate,enddate = EndDate, course = CourseObj,
                                    modulename = ModuleName,isActive = Active  )
        
                return Response({"msg":"Batch Created", "status":status.HTTP_201_CREATED})
            except Exception as e:
                return Response({"msg":"Batch not Created","error":e, "status":status.HTTP_417_EXPECTATION_FAILED})

        return Response({"msg":"Batch not Created","error":"Serializer is not Valid", "status":status.HTTP_401_UNAUTHORIZED})


class CreateTask(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        Serializer = CreateTaskSerializer(data=request.data)
        if Serializer.is_valid(raise_exception=True):
            try:
                BatchObj = Batch.objects.get(id = int(request.data["batch"]))
                StartDate = datetime.datetime.strptime(request.data["startdate"],"%Y-%m-%d %H:%M")
                EndDate =   datetime.datetime.strptime(request.data["enddate"],"%Y-%m-%d %H:%M")
                TaskCreatedBy = Account.objects.get(email = request.user)
                validated_data = request.data

                Task.objects.create(name = validated_data["name"], details = validated_data["details"],
                                    startdate = StartDate,enddate = EndDate, batch = BatchObj,
                                    task = validated_data["task"],createdby = TaskCreatedBy )

                return Response({"msg":"Task Created", "status":status.HTTP_201_CREATED})

            except Exception as e:
                return Response({"msg":"Tsk not Created","error":str(e), "status":status.HTTP_417_EXPECTATION_FAILED})

        return Response({"msg":"Task not Created","error":"Serializer is not Valid", "status":status.HTTP_401_UNAUTHORIZED})



class CreateExam(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        Serializer = CreateExamSerializer(data=request.data)
        if Serializer.is_valid(raise_exception=True):
            try:
                CourseObj= Courses.objects.get(id = int(request.data["course"]))
                BatchObj = Batch.objects.get(id = int(request.data["batch"]))
                ExamDate = datetime.datetime.strptime(request.data["examdate"],"%Y-%m-%d %I:%M")
                
                validated_data = request.data
                Exam.objects.create(name = validated_data["name"],details = validated_data["details"],examdate=ExamDate,duration = int(validated_data["duration"]),batch = BatchObj,course= CourseObj,
                                    firstquestion = validated_data["firstquestion"],firstqsnoptionone = validated_data["firstqsnoptionone"],firstqsnoptiontwo = validated_data["firstqsnoptiontwo"],firstqsnoptionthree = validated_data["firstqsnoptionthree"],firstqsnoptionfour = validated_data["firstqsnoptionfour"],firstqsnAnswer=validated_data["firstqsnAnswer"],
                                    secondquestion = validated_data["secondquestion"],secondqsnoptionone = validated_data["secondqsnoptionone"],secondqsnoptiontwo = validated_data["secondqsnoptiontwo"],secondqsnoptionthree = validated_data["secondqsnoptionthree"],secondqsnoptionfour = validated_data["secondqsnoptionfour"],secondqsnAnswer = validated_data["secondqsnAnswer"],
                                    thirdquestion = validated_data["thirdquestion"],thirdqsnoptionone = validated_data["thirdqsnoptionone"],thirdqsnoptiontwo = validated_data["thirdqsnoptiontwo"],thirdqsnoptionthree = validated_data["thirdqsnoptionthree"],thirdqsnoptionfour = validated_data["thirdqsnoptionfour"],thirdqsnAnswer = validated_data["thirdqsnAnswer"],
                                    fourthquestion = validated_data["fourthquestion"],fourthqsnoptionone = validated_data["fourthqsnoptionone"],fourthqsnoptiontwo = validated_data["fourthqsnoptiontwo"],fourthqsnoptionthree = validated_data["fourthqsnoptionthree"],fourthqsnoptionfour = validated_data["fourthqsnoptionfour"],fourthqsnAnswer = validated_data["fourthqsnAnswer"],
                                    fifthquestion = validated_data["fifthquestion"],fifthqsnoptionone = validated_data["fifthqsnoptionone"],fifthqsnoptiontwo = validated_data["fifthqsnoptiontwo"],fifthqsnoptionthree = validated_data["fifthqsnoptionthree"],fifthqsnoptionfour = validated_data["fifthqsnoptionfour"],fifthqsnAnswer = validated_data["fifthqsnAnswer"])
                return Response({"msg":"Exam Created", "status":status.HTTP_201_CREATED})
            except Exception as e:
                return Response({"msg":"Exam not Created","error":str(e), "status":status.HTTP_417_EXPECTATION_FAILED})

        return Response({"msg":"Exam not Created","error":"Serializer is not Valid", "status":status.HTTP_401_UNAUTHORIZED})

                
        






            

                    
                    

                    



