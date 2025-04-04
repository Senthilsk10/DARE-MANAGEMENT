from rest_framework import serializers
from .models import Dept, Fees, Student,Guide
from projects.models import Project
from projects.serializers import ProjectSerializer

class DeptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dept
        fields = '__all__'

class GuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guide
        fields = '__all__'

class FeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fees
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    active_project = serializers.SerializerMethodField()
    guide = serializers.PrimaryKeyRelatedField(
        queryset=Guide.objects.all()
    )
    guide_detail = GuideSerializer(source="guide", read_only=True)
    class Meta:
        model = Student
        fields = '__all__'

    def get_active_project(self, obj):
        projects = Project.objects.filter(student=obj, current = True).first()
        return ProjectSerializer(projects).data