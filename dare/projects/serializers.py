from rest_framework.serializers import (
    ModelSerializer,
    PrimaryKeyRelatedField,
    SerializerMethodField,
    CharField,
    Serializer
    )
from rest_framework import serializers
from .models import Project,Synopsis,Evaluator
from students.models import Student,Guide
from .crypt import cipher
import json
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
    encrypted = SerializerMethodField()
    # Use ID for input (write) but full object for output (read)
    student = PrimaryKeyRelatedField(
        queryset=Student.objects.all()
    )
    student_detail = StudentSerializer(source="student", read_only=True)

    guide = PrimaryKeyRelatedField(
        queryset=Guide.objects.all()
    )
    guide_detail = GuideSerializer(source="guide", read_only=True)
    class Meta:
        model = Project
        fields = '__all__'

    def get_encrypted(self, obj):
        data = {
            "student_id": obj.student.id,
            "project_id": obj.id
        }
        string = json.dumps(data).encode()
        encrypted_data = cipher.encrypt(string)
        return encrypted_data

class SynopsisSerializer(ModelSerializer):
    class Meta:
        model = Synopsis
        fields = '__all__'
        
class EvaluatorSerializer(ModelSerializer):
    class Meta:
        model = Evaluator
        exclude = ('status','last_sent_at','retry')
        
        

class MinimalMailToSendSerializer(serializers.Serializer):
    # Project Fields
    project_id = serializers.IntegerField(source='project.id')
    project_title = serializers.CharField(source='project.title')
    student_name = serializers.CharField(source='project.student.name')
    student_roll = serializers.IntegerField(source='project.student.roll')
    
    # Evaluator Fields
    evaluator_id = serializers.IntegerField()
    evaluator_name = serializers.CharField()
    evaluator_email = serializers.EmailField()
    evaluator_priority = serializers.IntegerField(source='priority')
    is_foreign = serializers.BooleanField(source='foreign_viva')
    
    # Mail Metadata
    mail_type = serializers.CharField()
    last_contact = serializers.DateTimeField(source='last_sent_at', required=False)
    attempt_count = serializers.IntegerField(source='retry')
    
    # Derived Fields
    email_subject = serializers.SerializerMethodField()
    
    def get_email_subject(self, obj):
        return (
            f"{obj['mail_type']}: Project Review - {obj['project'].title} "
            f"(Priority {obj['evaluator'].priority})"
        )