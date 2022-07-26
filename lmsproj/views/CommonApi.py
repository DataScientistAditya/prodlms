from ast import If
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from lmsproj.models import Account, Batch, BatchCourseAssign, Courses
from lmsproj.utils import GetProfileData, GetEventsData




class ProfileDetails(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        Id = request.user.id
        try:
            ObjectList = GetProfileData(userid=Id)
            print(ObjectList)
            return Response({"msg":"Profile data Scucessfully fetched","data":ObjectList, "status":status.HTTP_201_CREATED})
        except Exception as e:
            return Response({"msg":"Profile data not Scucessfully fetched","error":str(e), "status":status.HTTP_401_UNAUTHORIZED})



class GetEventsTeacherandBatchWise(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        Is_Admin = request.user.is_admin
        Data = GetEventsData(isAdmin=Is_Admin,userid=request.user.id)
        return Response({"msg":"Event data Scucessfully fetched","data":Data, "status":status.HTTP_201_CREATED})


class GetRelatedUserList(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        UserList = []
        BatchIds = BatchCourseAssign.objects.all().filter(user =  request.user.id).values("batch")
        for i in BatchIds:
            UserObjs = BatchCourseAssign.objects.select_related("user").filter(batch = i["batch"])
            for x in UserObjs:
                if x.user.id != request.user.id:
                    UserDetails = {
                        "id":x.user.id,
                        "label":x.user.username,
                    }
                    UserList.append(UserDetails)
        return Response({"msg":"Related Users Scucessfully fetched","data":UserList, "status":status.HTTP_201_CREATED})


#For creating batch
class GetCourseName(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        CourseObj = Courses.objects.all().values("id","name")
        AllCourse=[]
        for i in CourseObj:
            CoursenameData = {
                "id":i["id"],
                "label":i["name"],
            }
            AllCourse.append(CoursenameData)
        return Response({"msg":"Course Fetch Scucessfully fetched","data":AllCourse, "status":status.HTTP_201_CREATED})

#For Assiging Course and Batch
class GetUserAssignInputs(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        BatchObj = Batch.objects.all().values("id","name","modulename").order_by("-startdate")
        UserObjs =Account.objects.all().values("id","username")
        Listof_Batch = []
        Listof_Course = []
        Listof_User = []
        for x in UserObjs:
            Userdata = {
                "id":x["id"],
                "label":x["username"]
            }
            Listof_User.append(Userdata)
        for i in BatchObj:
            Data = {
                "id":i["id"],
                "label":i["name"]
            }
            CourseData={
                "id":i["id"],
                "modulename":i["modulename"],
                "coursename":Batch.objects.select_related("course").get(id = i["id"]).course.name
            }

            Listof_Batch.append(Data)
            Listof_Course.append(CourseData)
        return Response({"msg":"Batch Fetch Scucessfully fetched","data":Listof_Batch,"course":Listof_Course,"user":Listof_User, "status":status.HTTP_201_CREATED})

#for Exam inputs
class GetExamInputs(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        BatchObj = Batch.objects.all().values("id","name").order_by("-startdate")
        CourseObj = Courses.objects.all().values("id","name")
        AllCourse=[]
        Listof_Batch = []
        for i in CourseObj:
            CoursenameData = {
                "id":i["id"],
                "label":i["name"],
            }
            AllCourse.append(CoursenameData)
        for i in BatchObj:
            BatchData = {
                "id":i["id"],
                "label":i["name"]
            }
            Listof_Batch.append(BatchData)
        return Response({"msg":"Batch and Course data Scucessfully fetched","batch":Listof_Batch,"course":AllCourse, "status":status.HTTP_201_CREATED})



        
        









        
        

        
        

