from pyexpat import model
from attr import fields
from rest_framework import serializers
from lmsproj.models import TaskSubmission,ExamSubmit



class TsksubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskSubmission
        fields = ("taskanswer","task")

class ExamsubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model=ExamSubmit
        fields=("firstanswer","secondanswer","thirdasnswer","fourthanswer","fifthanswer")
