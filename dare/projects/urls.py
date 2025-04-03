from django.urls import path,include
from django.shortcuts import render
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'synopsis', SynopsisViewSet)
router.register(r'evaluators', EvaluatorViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path("file",get_project_files,name="project-files"),
    path('project/<int:project_id>/', lambda request, project_id: render(request, "projects/project.html", {"project_id": project_id})),
]
