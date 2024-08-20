from django.db import models
from datetime import datetime


class Department(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)

class Position(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    level = models.CharField(max_length=50, null=True, blank=True)

class Employee(models.Model):
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    hire_date = models.DateField(null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=3,null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE,null=True) #CASCADE:When the referenced object is deleted, also delete the objects that have references to it 
    position = models.ForeignKey(Position, on_delete=models.CASCADE,null=True)
    projects = models.CharField(max_length=50, null=True, blank=True)

    def str(self):
        return self.name
    
class Project(models.Model):
    NEW = "NW"
    ON_GOING = "OG"
    ENDED = "EN"
    Project_Status = {
        NEW: "New",
        ON_GOING: "On Going",
        ENDED: "Ended"
    }
    name = models.CharField(max_length=50, null=True, blank=True)
    team = models.ManyToManyField(Employee)
    team_lead = models.ForeignKey(Employee, related_name='%(class)s_requests_created',on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=Project_Status)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    