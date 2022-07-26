from rest_framework import serializers
from lmsproj.models import BatchCourseAssign





class BatchCourseAssignSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatchCourseAssign
        fields = ("batch","course","activeModule","user")
