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
    path("webhook/synopsis",synopsis_webhook,name="synopsis-files"),
    path("webhook/project",project_webhook,name="project-files"),
    path('projects/',projects,name="projects"),
    path('project/<int:project_id>/',project_detail_view,name="project-info"),
    path('api/mailtosend', MailToSendView.as_view(), name='mail_to_send'),
    path("api/acknowledgemail",acknowledge_mail,name="mail-reciept"),
    path("api/awaitingresponse",PendingEvaluatorsView.as_view(),name="mail-to-read"),
    path("api/acknowledgeresponse",receive_email_responses,name="response-reciept"),
]
