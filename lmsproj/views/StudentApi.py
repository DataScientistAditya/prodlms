
from rest_framework.views import APIView
from yaml import serialize
from lmsproj.models import Account, Exam, ExamSubmit, Task, TaskSubmission
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from lmsproj.models import Account, TaskSubmission, Task
from lmsproj.studentserializer import TsksubmissionSerializer, ExamsubmissionSerializer
from lmsproj.utils import GetCompletedandPendingTask,GetExamData




class TaskSubmit(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request):
        Serializer = TsksubmissionSerializer(data=request.data)
        if Serializer.is_valid(raise_exception=True):
            validated_data = request.data
            try:
                UserObj = Account.objects.get(email= request.user)
                TaskObj = Task.objects.get(id = int(validated_data["task"]))

                TaskSubmission.objects.create(student = UserObj, taskanswer = validated_data["taskanswer"],task = TaskObj )
                return Response({"msg":"Task Successfully Submited", "status":status.HTTP_201_CREATED})
            except Exception as e:
                return Response({"msg":"Task Successfully Submited","error":e, "status":status.HTTP_401_UNAUTHORIZED})

            
        else:
            return Response({"msg":"Serializer is not valid", "status":status.HTTP_417_EXPECTATION_FAILED})


class AllTaskinfo(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        CurrentStudent_Id= request.user.id
        Completed,Pending = GetCompletedandPendingTask(studentid=CurrentStudent_Id)
        return Response({"msg":"Student Task","data":{"completed":Completed,"pending":Pending}, "status":status.HTTP_201_CREATED})


class AllExamInfo(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        ExamData = GetExamData(userid=request.user.id)
        return Response({"msg":"Student Exam Details","data":ExamData, "status":status.HTTP_201_CREATED})


class StudentExamSubmit(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        Serializer = ExamsubmissionSerializer(data=request.data)
        if Serializer.is_valid(raise_exception=True):
            validated_data = request.data
            userobj = Account.objects.get(id = request.user.id)
            examobj = Exam.objects.get(id = int(validated_data["examid"]))
            Listof_RightAnswer = [examobj.firstqsnAnswer, examobj.secondqsnAnswer, examobj.thirdqsnAnswer, examobj.fourthqsnAnswer , examobj.fifthqsnAnswer]
            Listof_Answer = [validated_data["firstanswer"],validated_data["secondanswer"],validated_data["thirdasnswer"],validated_data["fourthanswer"], validated_data["fifthanswer"]]
            ScoreList = Listof_RightAnswer - Listof_Answer
            Score = len(ScoreList)
            try:
                ExamSubmit.objects.create(student = userobj, 
                                            exam = examobj, 
                                            firstanswer = validated_data["firstanswer"],
                                            secondanswer = validated_data["secondanswer"],
                                            thirdasnswer = validated_data["thirdasnswer"],
                                            fourthanswer = validated_data["fourthanswer"],
                                            fifthanswer = validated_data["fifthanswer"],
                                            grade = Score )
                return Response({"msg":"Exam Submitted Successfully", "status":status.HTTP_201_CREATED})
            except Exception as e:
                return Response({"msg":"Exam not Submitted Successfully", "data":str(e) ,"status":status.HTTP_417_EXPECTATION_FAILED})


        else:
            return Response({"msg":"Serializer is not valid", "status":status.HTTP_400_BAD_REQUEST})

            

            

        











