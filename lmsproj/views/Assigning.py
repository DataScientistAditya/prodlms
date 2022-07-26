from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from lmsproj.assiginingserializer import BatchCourseAssignSerializer
from lmsproj.models import Account, Batch, Courses,BatchCourseAssign



# if user id found then it should update it
class AssignUser(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        Serializer = BatchCourseAssignSerializer(data=request.data)
        if Serializer.is_valid(raise_exception=True):
            validated_data = request.data
            print(validated_data)
            # try:
            BatchObj = Batch.objects.get(id = int(validated_data["batch"]))
            CourseObj = Courses.objects.get(id = int(validated_data["course"]))
            UserObj = Account.objects.get(id = int(validated_data["user"]))
            try:
                AssignObj = BatchCourseAssign.objects.filter(user =int(validated_data["user"])).filter(course = int(validated_data["course"]))
                if len(AssignObj)>0:
           
                    BatchCourseAssign.objects.filter(user =int(validated_data["user"])).update(batch = BatchObj, course = CourseObj,activeModule= validated_data["activeModule"])
                    return Response({"msg":"Course Batch and Module is Updated", "status":status.HTTP_201_CREATED})
                else:
                    BatchCourseAssign.objects.create(batch = BatchObj,course = CourseObj,activeModule= validated_data["activeModule"],user = UserObj)
                    return Response({"msg":"Course Batch and Module is Assigned", "status":status.HTTP_201_CREATED})
            except Exception as e:
                return Response({"msg":"Course Batch and Module is not Assigned","error":str(e), "status":status.HTTP_417_EXPECTATION_FAILED})

        return Response({"msg":"Course Batch and Module is not Assigned","error":"Serializer is not Valid", "status":status.HTTP_401_UNAUTHORIZED})
