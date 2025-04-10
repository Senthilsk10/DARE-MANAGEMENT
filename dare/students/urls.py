from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DeptViewSet, FeesViewSet, StudentViewSet,GuideViewSet
from .views import DeptView,department
from django.shortcuts import render
router = DefaultRouter()
router.register(r'depts', DeptViewSet)
router.register(r'fees', FeesViewSet)
router.register(r'students', StudentViewSet)
router.register(r'guides', GuideViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('departments/',DeptView.as_view(),name="departments"),
     path('department/<int:dept_id>/',department,name="dept")
]
