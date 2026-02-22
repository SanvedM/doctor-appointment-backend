from rest_framework import serializers
from .models import *


class RegisterSerializers(serializers.ModelSerializer):

    password = serializers.CharField(write_only = True,min_length = 8)
    class Meta:
        model = CustomeUser
        fields = ("username","password","first_name","last_name","email","mobile_no","role")

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = CustomeUser.objects.create(**validated_data)

        user.set_password(password)

        user.save()
        return user
    
class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomeUser
        # exclude =("password","is_active","user_permissions","groups","role")
        fields = ("id","username","first_name","last_name","date_joined","email","mobile_no","role")

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ("department_name","description")


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    department = DepartmentSerializer(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(),
        source="department",
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = ProfileDetails
        fields = ["id","user", "department", "department_id", "qualification", "experience", "fee"]

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["user"] = request.user
        return super().create(validated_data)

class AppointmentSerializer(serializers.ModelSerializer):

    doctor = serializers.PrimaryKeyRelatedField(
        source="admin",
        queryset=CustomeUser.objects.filter(role="doctor")
    )

    admin_username = serializers.CharField(source="admin.username", read_only=True)
    customer_username = serializers.CharField(source="customer.username", read_only=True)

    class Meta:
        model = AppointmentDetails
        fields = (
            "id",
            "doctor",
            "admin_username",
            "customer",
            "customer_username",
            "appointment_date",
            "appointment_time",
            "status",
        )




class MyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomeUser
        fields = ("username", "first_name", "email", "mobile_no")