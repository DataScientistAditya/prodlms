from ast import Return
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Chat.models import MessageData
from lmsproj.models import Account
from Chat.serializers import MessegeSerializer



# Create your views here.
class Index(APIView):
    def get(self, request):
        return Response({"msg":"Msg Data","data":request.data, "status":status.HTTP_201_CREATED})

class ChatMessege(APIView):
    def get(self, request, room_name):
        Messefes_PREV = MessageData.last_20_messages(room_name=room_name)
        MsgData = {
            'room_name': room_name,
            'username': request.user.username,
            'msg': Messefes_PREV,
        }
        return Response({"msg":"Msg Data","data":MsgData, "status":status.HTTP_201_CREATED})

class AllRooms(APIView):
    permission_classes= [IsAuthenticated]
    def get(self,request):
        UserObj = Account.objects.get(id = request.user.id)
        AllRooms = MessageData.objects.all().filter(Author = UserObj).values("roomname")
        return Response({"msg":"All Rooms","data":AllRooms, "status":status.HTTP_201_CREATED})


class SaveMesseges(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        Serializer = MessegeSerializer(data=request.data)
        if Serializer.is_valid(raise_exception=True):
            UserObj = Account.objects.get(id = request.user.id)
            FriendUserObj= Account.objects.get(username = validated_data["friend"])
            validated_data = request.data
            MessageData.objects.create(Author = UserObj, content = validated_data["content"], roomname = validated_data["roomname"],friend = validated_data["friend"])
            MessageData.objects.create(Author = FriendUserObj, content = validated_data["content"], roomname = validated_data["roomname"],friend = request.user.username)
            return Response({"msg":"Messege data saved","status":status.HTTP_201_CREATED})
        return Response({"msg":"Messege data not saved, serializer is not valid","status":status.HTTP_405_METHOD_NOT_ALLOWED})


            

        

        
        
    
