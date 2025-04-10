from django.shortcuts import render
from students.models import Student, Guide
from .models import Project, Evaluator,Synopsis
from .serializers import *
from rest_framework import viewsets
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from .crypt import cipher
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q,Max
from django.db import models
from mails.models import Mail,Reply
from datetime import datetime
from django.contrib.auth.decorators import login_required
"""
Every function that uses project should verify on current field to be true to operate the project,
only the current project should be worked on
"""

@login_required
def projects(request):
    return render(request,"projects/projects.html")

@login_required
def project_detail_view(request, project_id):
    return render(request, "projects/project.html", {"project_id": project_id})

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

@csrf_exempt
def project_webhook(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            # print(data)
            decrypted = json.loads(cipher.decrypt(data["form-details"]).decode())
            # print(decrypted)
            # print(type(decrypted))
            pr_id = decrypted.get('project_id')
            project = Project.objects.get(id=pr_id)
            link = data['upload your Project PDF file'][0]
            project.file_link = link
            project.save()
            return JsonResponse({"message": "success"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def acknowledge_mail(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            project_id = data.get('project')
            to_id = data.get('to')
            content = data.get('content')
            subject = data.get('subject', 'Not Mentioned')
            message_id = data.get('message_id')

            if not all([project_id, to_id, content, message_id]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            project = Project.objects.get(id=project_id)
            evaluator = Evaluator.objects.get(id=to_id)

            Mail.objects.create(
                project=project,
                to=evaluator,
                content=content,
                subject=subject,
                message_id=message_id
            )
            
            if evaluator.retry == 0:
                evaluator.status = "APPROACHED"
            else:
                evaluator.status = "REMAINDERED"
            
            evaluator.retry += 1
            evaluator.last_sent_at = datetime.now()
            evaluator.save()
            

            return JsonResponse({'message': 'Acknowledgment saved successfully'}, status=201)

        except Project.DoesNotExist:
            return JsonResponse({'error': 'Project not found'}, status=404)
        except Evaluator.DoesNotExist:
            return JsonResponse({'error': 'Evaluator not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)

from datetime import timedelta
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response

class MailToSendView(APIView):
    def get(self, request):
        now = timezone.now()
        wait_period = now - timedelta(days=15)

        results = []

        # Step 1: Get all eligible projects
        projects = Project.objects.filter(
            closed=False,
            guide_approved=True,
            file_link__isnull=False
        ).select_related('student')
        # results.append(projects.values_list())
        for project in projects:
            # Separate evaluators by type, ordered by priority
            foreign_evs = project.evaluator_set.filter(foreign_viva=True).order_by('priority')
            local_evs = project.evaluator_set.filter(foreign_viva=False).order_by('priority')

            # Check foreign evaluator logic
            fev = get_eligible_evaluator(foreign_evs, wait_period)
            # print(fev) # proble here
            if fev:
                results.append(build_entry(project, fev))

            # Check local evaluator logic
            lev = get_eligible_evaluator(local_evs, wait_period)
            if lev:
                results.append(build_entry(project, lev))

        return Response(results)


def get_eligible_evaluator(evaluators, wait_period):
    for ev in evaluators:
        if ev.status in ['IDLE', 'APPROACHED', 'REMAINDERED'] and ev.retry < 3:
            if ev.last_sent_at is None or ev.last_sent_at < wait_period:
                return ev
            else:
                # Evaluator was already mailed recently, block this type
                return None
        elif ev.status == 'REJECTED':
            continue  # move to next evaluator
        else:
            break  # don't proceed past accepted ones
    return None


def build_entry(project, ev):
    student = project.student
    mail_type = 'APPROACH' if ev.retry == 0 else 'REMINDER'
    synopsis = Synopsis.objects.filter(project=project,current=True).first()
    return {
        "project_id": project.id,
        "project_ref_id":project.referel_id,
        "project_title": project.title,
        "synopsis_file":synopsis.file_link,
        "synopsis_title":synopsis.title,
        "student_name": student.name,
        "student_roll": student.roll,
        "student_dept":student.dept.name,
        "student_guide":student.guide.name,
        "evaluator_id": ev.id,
        "evaluator_name": ev.name,
        "evaluator_email": ev.email,
        "is_foreign": ev.foreign_viva,
        "mail_type": mail_type,
        "last_contact": ev.last_sent_at.isoformat() if ev.last_sent_at else None,
        "attempt_count": ev.retry
    }


class PendingEvaluatorsView(APIView):
    def get(self, request, format=None):
        fifteen_days_ago = datetime.now() - timedelta(days=15)
        result = []

        # Loop through all projects
        for project in Project.objects.all():
            # Find evaluators of this project who were emailed within last 15 days and haven't completed viva
            evaluators = Evaluator.objects.filter(
                project=project,
                last_sent_at__gte=fifteen_days_ago, 
                is_viva=False
            ).exclude(status__in=['REJECTED','ACCEPTED'])

            for evaluator in evaluators:
                result.append({
                    "project_id": project.id,
                    "ref":project.referel_id,
                    "evaluator_email": evaluator.email
                })

        return Response(result)
    

@csrf_exempt
def receive_email_responses(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            if data:
                print(data)
                for entry in data:
                    project = Project.objects.filter(referel_id=entry['ref_id']).first()
                    if not project:
                        return JsonResponse({"status": "Failed", "message": "Invalid project referel id"}, status=200)

                    evaluator = Evaluator.objects.filter(project=project, email=entry['classification']['email']).first()
                    if not evaluator:
                        return JsonResponse({"status": "Failed", "message": "Invalid evaluator Email id"}, status=200)

                    # Create a Response object
                    response_obj = Reply(
                        project=project,
                        evaluator=evaluator,
                        response=entry['body'],
                        attachments=entry['attachments'],
                        subject=entry['subject'],
                        message_id=entry['msg_id'],
                    )
                    response_obj.save()

                    # Update Evaluator status based on classification
                    if 'classification' in entry:
                        if entry['classification']['status'] == "accepted":
                            evaluator.status = "ACCEPTED"
                            evaluator.is_viva = True
                            evaluator.save()
                        elif entry['classification']['status'] == "rejected":
                            evaluator.status = "REJECTED"
                            evaluator.save()

                return JsonResponse({"status": "success", "message": "Replies received and processed"}, status=200)
            else:
                return JsonResponse({"error": "Invalid payload format"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    else:
        return JsonResponse({"error": "Only POST allowed"}, status=405)