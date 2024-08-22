from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework.views import APIView
from .models import Employee, Department, Project
from django.shortcuts import get_object_or_404
from django.db.models import Max, F, Subquery, OuterRef, Sum
from .serializers import (  CreateEmployeeSerializer, MinimalEmployeeSerializer, DetailEmployeeSerializer, UpdateEmployeeSerializer, DepartmentEmployeeSerializer, CreateDepartmentSerializer,
     DepartmentSerializer,DetailDepartmentSerializer, UpdateDepartmentSerializer, ProjectSerializer, CreateProjectSerializer
)

class EmployeeListSet(APIView):
    def get(self, request):
        queryset = Employee.objects.all()
        serializer = MinimalEmployeeSerializer(queryset, many =True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CreateEmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EmployeeRetrieveSet(APIView):
    def get_object(self, pk):
        return Employee.objects.get(pk=pk)
    
    def get(self, request, pk=None):
        queryset =  self.get_object(pk)    
        serializer =  DetailEmployeeSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)         

    def put(self, request, pk=None):
        queryset =  self.get_object(pk) 
        serializer = UpdateEmployeeSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk=None):
        employee =  self.get_object(pk) 
        employee.delete()
        return Response(f"Employee is deleted having id {pk}", status=status.HTTP_204_NO_CONTENT)
    
class EmployeeDepartmentListSet(APIView):
    def get_object(self, pk):
        return Employee.objects.get(pk=pk)
    
    def get(self, request, pk=None):
        queryset =  self.get_object(pk) 
        serializer = DepartmentEmployeeSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class SecondHighestSalaryByDepartmentView(APIView):
    def get(self, request):
        subquery = Employee.objects.filter(
            department=OuterRef('department')
        ).order_by('-salary').values('salary')[1:2]

        employees = Employee.objects.annotate(
            second_highest_salary=Subquery(subquery)
        ).filter(
            salary=F('second_highest_salary')
        )

        serializer = DetailEmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class DepartmentViewSet(APIView):
    def get(self, request):
        queryset = Department.objects.all()
        serializer = DepartmentSerializer(queryset, many =True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CreateDepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DepartmentRetrieveSet(APIView):
    def get_object(self, pk):
        return Department.objects.get(pk=pk)
    
    def get(self, request, pk=None):
        queryset =  self.get_object(pk)    
        serializer =  DetailDepartmentSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)         

    def put(self, request, pk=None):
        queryset =  self.get_object(pk) 
        serializer = UpdateDepartmentSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk=None):
        Department =  self.get_object(pk) 
        Department.delete()
        return Response(f"Department is deleted having id {pk}", status=status.HTTP_204_NO_CONTENT)

class TotalSalaryByDepartmentView(APIView):
    def get(self, request):
        departments = Department.objects.annotate(
            total_salary=Sum('employee__salary')
        )

        data = [
            {
                'department_id': department.id,
                'department_name': department.name,
                'total_salary': department.total_salary
            }
            for department in departments
        ]

        return Response(data, status=status.HTTP_200_OK)

# class ProjectViewSet(APIView):
#     def get(self, request):
#         queryset = Project.objects.all()
#         serializer = ProjectSerializer(queryset, many =True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         serializer = CreateProjectSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectViewSet(APIView):
    def get(self, request, pk=None):
        if pk is None:
            queryset = Project.objects.all()
            serializer = ProjectSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            project = self.get_object(pk)
            serializer = ProjectSerializer(project)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        project = self.get_object(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def add_member(self, request, pk=None):
        project = self.get_object(pk)
        employee_id = request.data.get('employee_id')
        employee = get_object_or_404(Employee, id=employee_id)
        project.team.add(employee)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def update_status(self, request, pk=None):
        project = self.get_object(pk)
        status = request.data.get('status')
        project.status = status
        project.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self, pk):
        return get_object_or_404(Project, pk=pk)

class AddMemberToProjectView(APIView):
    def put(self, request, pk=None):
        project = get_object_or_404(Project, pk=pk)
        employee_id = request.query_params.get('employee_id')
        if not employee_id:
            return Response({"error": "employee_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        print(f"Employee ID: {employee_id}")
        employee = get_object_or_404(Employee, id=employee_id)
        project.team.add(employee)
        
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProjectBudgetView(APIView):
    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        total_budget = project.employees.aggregate(total_budget=Sum('salary'))['total_budget']
        return Response({'project_id': pk, 'total_budget': total_budget}, status=status.HTTP_200_OK)

class NewProject(APIView):
    def get(self, request):
        print(request.query_params)
        projects = Project.objects.filter(status="NW")
        serializer = ProjectSerializer(projects,many=True)  
        return Response(serializer.data, status=status.HTTP_200_OK)

class OngoingProject(APIView):
    def get(self, request):
        print(request.query_params)
        projects = Project.objects.filter(status="OG")
        serializer = ProjectSerializer(projects,many=True)  
        return Response(serializer.data, status=status.HTTP_200_OK)

class EndedProject(APIView):
    def get(self, request):
        print(request.query_params)
        projects = Project.objects.filter(status="EN")
        serializer = ProjectSerializer(projects,many=True)  
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class HighestSalary(APIView):
    def get(self, request):
        print(request.query_params)
        employee = Employee.objects.order_by('salary').first()
        serializer = DetailEmployeeSerializer(employee)  
        return Response(serializer.data, status=status.HTTP_200_OK)


class PositionViewSet(APIView):
    pass

#jenkins