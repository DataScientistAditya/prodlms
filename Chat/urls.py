from django.urls import path
from Chat.views import ChatMessege, AllRooms,Index


urlpatterns =[
    path('', Index.as_view(), name='index'),
    path('<str:room_name>/', ChatMessege.as_view(), name='room'),
    path('allrooms/', AllRooms.as_view(), name='allrooms'),
]