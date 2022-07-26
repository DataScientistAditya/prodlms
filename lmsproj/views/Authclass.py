from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from lmsproj.authserializers import RegisterSerializer
from django.contrib.auth import login, logout
from lmsproj.utils import get_tokens_for_user, ValidateUser
# from lmsproj.models import Account



class Signup(APIView):
    def post(self, request):
        Serializer = RegisterSerializer(data=request.data)
        if Serializer.is_valid():
            Serializer.create(validated_data=request.data)
            return Response({"msg":"User Created","data":Serializer.data, "status":status.HTTP_201_CREATED})

        return Response(Serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   

class SignIn(APIView):
    def post(self,request):
        email = request.data["email"]
        password = request.data["password"]
        # print(email,password)
        user = ValidateUser(Email=email, Password=password)
        # print("user validated")
        # print(user)
        if user is not None:
            login(request, user=user)
            authdata = get_tokens_for_user(user=user)
            Data={
                
                "id":user.id,
                "email":user.email,
                "username":user.username,
                "isTeacher":user.isTeacher,
                "isStudent":user.isStudent,
                "isAdmin":user.is_admin,

            }
            return Response({'msg': 'Login Success',"data":Data, **authdata}, status=status.HTTP_200_OK)

        return Response({'msg': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class SignOut(APIView):
    def get(self, request):
        logout(request)
        return Response({'msg': 'Successfully Logged out'}, status=status.HTTP_200_OK)



