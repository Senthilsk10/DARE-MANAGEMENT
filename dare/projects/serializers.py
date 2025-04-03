from rest_framework.serializers import ModelSerializer,PrimaryKeyRelatedField
from .models import Project,Synopsis,Evaluator
from students.models import Student,Guide

class GuideSerializer(ModelSerializer):
    class Meta:
        model = Guide
        fields = '__all__'
        
class StudentSerializer(ModelSerializer):
    guide = GuideSerializer()
    class Meta:
        model = Student
        fields = '__all__'

class ProjectSerializer(ModelSerializer):
    student = PrimaryKeyRelatedField(queryset=Student.objects.all())
    guide = PrimaryKeyRelatedField(queryset=Guide.objects.all())
    class Meta:
        model = Project
        fields = '__all__'

class SynopsisSerializer(ModelSerializer):
    class Meta:
        model = Synopsis
        fields = '__all__'
        
class EvaluatorSerializer(ModelSerializer):
    class Meta:
        model = Evaluator
        fields = '__all__'