from rest_framework.serializers import ModelSerializer,PrimaryKeyRelatedField,SerializerMethodField
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
    student = PrimaryKeyRelatedField(queryset=Student.objects.all())
    guide = PrimaryKeyRelatedField(queryset=Guide.objects.all())
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
        fields = '__all__'