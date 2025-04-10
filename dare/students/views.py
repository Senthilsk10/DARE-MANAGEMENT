from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import *
from rest_framework import viewsets
from .models import Dept, Fees, Student
from .serializers import DeptSerializer, FeesSerializer, StudentSerializer,GuideSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator

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

# method_decorator(login_required,name="dispatch")

class DeptView(LoginRequiredMixin,TemplateView):
    template_name = "dept.html"


@login_required
def department(request, dept_id): 
    name = Dept.objects.get(id=dept_id).name
    return render(request, "dept-info.html", {"dept_id": dept_id,"dept_name":name})