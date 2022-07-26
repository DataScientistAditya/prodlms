from pyexpat import model
from attr import fields
from rest_framework import serializers
from Chat.models import MessageData



class MessegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageData
        fields = ("content","roomname")

