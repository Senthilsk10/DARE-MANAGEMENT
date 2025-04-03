from django.shortcuts import render
from students.models import Student, Guide
from .models import Project, Evaluator,Synopsis
from .serializers import *
from rest_framework import viewsets
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from .crypt import cipher
"""
Every function that uses project should verify on current field to be true to operate the project,
only the current project should be worked on
"""

@csrf_exempt
def synopsis_webhook(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            print(data)
            decrypted = json.loads(cipher.decrypt(data["form-details"]).decode())
            print(decrypted)
            print(type(decrypted))
            pr_id = decrypted.get('project_id')
            project = Project.objects.get(id=pr_id)
            Synopsis.objects.create(project=project,file_link=data['upload your synopsis PDF file'][0],title=data['Title'])
            return JsonResponse({"message": "success"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

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

