from django.core.management.base import BaseCommand
from students.models import Student, Guide,Dept, Fees, Collection
from projects.models import Evaluator, Project, Synopsis
from django.utils.timezone import now
from django.contrib.auth.models import User 

class Command(BaseCommand):
    help = "Populate the database with sample data"
    def handle(self, *args, **kwargs):
        User.objects.create_superuser('admin', 'admin@example.com', 'admin')
        # Create Departments
        cs_dept = Dept.objects.create(name="Computer Science", min_years=3, max_years=5)
        ec_dept = Dept.objects.create(name="Electronics", min_years=3, max_years=5)
        
        # Create Fees
        Fees.objects.create(dept=cs_dept, sem=1, fees=50000)
        Fees.objects.create(dept=cs_dept, sem=2, fees=50000)
        
        Fees.objects.create(dept=ec_dept, sem=1, fees=48000)
        
        # Create Guides
        guide1 = Guide.objects.create(name="Dr. Smith", email="smith@example.com", phone="1234567890",dept=cs_dept)
        guide2 = Guide.objects.create(name="Dr. Jane", email="jane@example.com", phone="0987654321",dept=ec_dept)
        
        # Create Students
        student1 = Student.objects.create(name="Alice", roll=101, dept=cs_dept,mail="alice@gmail.com",guide=guide1)
        student2 = Student.objects.create(name="Bob", roll=102, dept=ec_dept,mail="bob@gmail.com",guide=guide2)
        
        # Create Projects
        project1 = Project.objects.create(student=student1, guide=guide1, file_link="http://example.com/project1",title="My PHD Project")
        project2 = Project.objects.create(student=student2, guide=guide2, file_link="http://example.com/project2",title="My PHD Project")
        
        # Create Evaluators
        evaluator1 = Evaluator.objects.create(project=project1,name="Prof. Xavier", email="xavier@example.com", phone="1111111111", foreign_viva=False)
        evaluator2 = Evaluator.objects.create(project=project1,name="Dr. Logan", email="logan@example.com", phone="2222222221", foreign_viva=True)
        evaluator1 = Evaluator.objects.create(project=project1,name="Prof. Joe", email="joe@example.com", phone="1111111112", foreign_viva=False)
        evaluator2 = Evaluator.objects.create(project=project1,name="Dr. Tony", email="Tony@example.com", phone="2222222222", foreign_viva=True)
        evaluator1 = Evaluator.objects.create(project=project1,name="Prof. May", email="may@example.com", phone="1111111113", foreign_viva=False)
        evaluator2 = Evaluator.objects.create(project=project1,name="Dr. Reed", email="reed@example.com", phone="2222222223", foreign_viva=True)
        evaluator1 = Evaluator.objects.create(project=project1,name="Prof. Peter", email="peter@example.com", phone="1111111114", foreign_viva=False)
        evaluator2 = Evaluator.objects.create(project=project1,name="Dr. Francis", email="francis@example.com", phone="2222222224", foreign_viva=True)
        
        # Create Synopses
        Synopsis.objects.create(project=project1, file_link="http://example.com/synopsis1")
        Synopsis.objects.create(project=project2, file_link="http://example.com/synopsis2")
        
        # Create Collections
        fee1 = Fees.objects.get(dept=cs_dept, sem=1)
        Collection.objects.create(student=student1, fee=fee1, amount=50000, fine=0, received_at=now())
        
        self.stdout.write(self.style.SUCCESS("Successfully populated the database with sample data"))
