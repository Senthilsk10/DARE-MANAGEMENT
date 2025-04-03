from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import *
from rest_framework import viewsets
from .models import Dept, Fees, Student
from .serializers import DeptSerializer, FeesSerializer, StudentSerializer,GuideSerializer
from django_filters.rest_framework import DjangoFilterBackend

class DeptViewSet(viewsets.ModelViewSet):
    queryset = Dept.objects.all()
    serializer_class = DeptSerializer

class FeesViewSet(viewsets.ModelViewSet):
    queryset = Fees.objects.all()
    serializer_class = FeesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['dept']

class GuideViewSet(viewsets.ModelViewSet):
    queryset = Guide.objects.all()
    serializer_class = GuideSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['dept']
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['dept']

from django.shortcuts import render
from django.views.generic import TemplateView

class DeptView(TemplateView):
    template_name = "dept.html"
