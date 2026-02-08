from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomeUser(AbstractUser):
    ROLE_CHOICES = (
        ("customer", "Customer"),
        ("doctor", "Doctor"),  # doctor
        ("staff", "Staff"),  # doctor

    )

    email = models.EmailField(unique=True)
    mobile_no = models.CharField(max_length=11, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="customer")

    def is_doctor(self):
        return self.role == "staff"
    
    def __str__(self):
        return self.username


class Department(models.Model):
    department_name =  models.CharField(max_length=20,null= True,blank=True)
    description = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.department_name

class ProfileDetails(models.Model):
    user = models.ForeignKey(CustomeUser,on_delete=models.CASCADE)
    department = models.ForeignKey(Department,on_delete=models.SET_NULL,null=True,blank=True)
    qualification = models.CharField(max_length=50,null=True,blank=True)
    experience = models.IntegerField(null=True,blank=True)
    fee = models.IntegerField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return self.user.username
    
class SheduleDetails(models.Model):
    admin = models.ForeignKey(CustomeUser, on_delete=models.CASCADE,  limit_choices_to={"role": "staff"},related_name="schedules")
    day_of_week = models.CharField(max_length=20,null=True,blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.admin.username} - {self.day_of_week}"
    
class AppointmentDetails(models.Model):

    ROLE_CHOICES = (
        ("pending", "Pending"),
        ("confirm", "Confirm"),
        ("reject", "Reject"),
    )

    admin = models.ForeignKey(CustomeUser, on_delete=models.CASCADE,limit_choices_to={"role": "doctor"}, related_name="admin_appointments")
    customer = models.ForeignKey(CustomeUser, on_delete=models.CASCADE,limit_choices_to={"role": "customer"}, related_name="user_appointments",null=True,blank=True)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=20,choices=ROLE_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer.username} - {self.appointment_date}"