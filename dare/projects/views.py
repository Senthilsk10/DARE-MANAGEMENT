from django.shortcuts import render
from students.models import Student, Guide
from .models import Project, Evaluator,Synopsis
from .serializers import *
from rest_framework import viewsets
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
"""
Every function that uses project should verify on current field to be true to operate the project,
only the current project should be worked on
"""

@csrf_exempt
def get_project_files(request):
    print(request.POST)
    return JsonResponse({"message":"success"},safe=False,status=200)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['student','current']
    
class SynopsisViewSet(viewsets.ModelViewSet):
    queryset = Synopsis.objects.all()
    serializer_class = SynopsisSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project','current']

class EvaluatorViewSet(viewsets.ModelViewSet):
    queryset = Evaluator.objects.all()
    serializer_class = EvaluatorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project']
