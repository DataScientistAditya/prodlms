from rest_framework import serializers
from lmsproj.models import Account



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ("email","username","firstname","lastname","phonenumber")


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ("email","username","firstname","lastname","phonenumber","isTeacher","isStudent","password")
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        if validated_data["isTeacher"] == "1":
            Teacher = True
            Student = False
        else:
            Teacher = False
            Student = True
        user = Account(email = validated_data["email"],
                                    username = self.validated_data["username"], 
                                    firstname = validated_data["firstname"],
                                    lastname = validated_data["lastname"],
                                    phonenumber = validated_data["phonenumber"] ,
                                    isStudent = Student,
                                    isTeacher = Teacher ,)

        user.set_password( validated_data["password"])
        user.save()
        return user


