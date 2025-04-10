from django.db import models
from django.contrib.auth.models import AbstractUser 

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('student', 'Student'),
        ('evaluator', 'Evaluator'),
        ('guide', 'Guide'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

class Dept(models.Model):
    name = models.CharField(max_length=255, unique=True)
    min_years = models.IntegerField()
    max_years = models.IntegerField()


    # implement fees getter for students with -> id -> sem num - > return fees 
    # first check wheter the sem fees were added upto max years -> max_yers= 8 then 8*2 sem 16 sems (16 fees objects should be there)   
    def fee(self, sem):
        pass
    def __str__(self):
        return self.name

class Fees(models.Model):
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE)
    sem = models.IntegerField()
    fees = models.IntegerField()

    class Meta:
        unique_together = ('dept', 'sem')  # Ensure unique semester fees

class Guide(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True,null=False)
    phone = models.CharField(max_length=15, unique=True,null=False)
    dept = models.ForeignKey(Dept,on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=255)
    roll = models.IntegerField(unique=True)
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE)
    sem = models.IntegerField(default=1)
    mail = models.EmailField(unique=True,null=False)
    guide = models.ForeignKey(Guide,on_delete=models.PROTECT)
    def __str__(self):
        return f"{self.name} ({self.roll})"

class Collection(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    fee = models.ForeignKey(Fees, on_delete=models.CASCADE)
    amount = models.IntegerField()
    fine = models.IntegerField(default=0)
    received_at = models.DateTimeField(auto_now_add=True)
