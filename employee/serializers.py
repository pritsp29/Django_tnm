from django.db.models import fields
from rest_framework import serializers
from .models import Employee, Department, Position, Project

class CreateEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"
        
class MinimalEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"
        
class DetailEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"
        
class UpdateEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["id", "first_name", "last_name", "email", "phone_number"]

# class DepartmentEmployeeSerializer(serializers.ModelSerializer):
#     # data = serializers.StringRelatedField(many=True)
#     # employee = DetailEmployeeSerializer()
#     class Meta:
#         model = Department
#         # fields = ["name","location","employee"]
#         fields= "__all__"


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__" 

class DepartmentEmployeeSerializer(serializers.ModelSerializer):
    # data = serializers.StringRelatedField(many=True)
    department = DepartmentSerializer()
    class Meta:
        model = Employee
        # fields = ["name","location","employee"]
        fields= "__all__"


class CreateDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__" 

class DetailDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__" 

class UpdateDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__" 

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__" 

class CreateProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__" 

# class PositionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Position
#         fields = ('tital','level')   