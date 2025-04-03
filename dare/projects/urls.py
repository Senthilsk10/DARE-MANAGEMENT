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
    path("webhook/synopsis",synopsis_webhook,name="project-files"),
    path('project/<int:project_id>/', lambda request, project_id: render(request, "projects/project.html", {"project_id": project_id})),
    path('view/file/<str:file_id>', lambda request, file_id: render(request, "iframe.html", {"file_id": file_id})),
]
