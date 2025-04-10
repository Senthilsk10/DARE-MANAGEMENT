from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from students.models import Student,Guide
from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator

class Project(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE)
    title  = models.CharField(max_length=200,null=False,blank=False)
    file_link = models.CharField(max_length=200,null=True,blank=True)
    uploaded_at = models.DateTimeField( auto_now_add=True)
    current = models.BooleanField(default=True)
    guide_approved = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)
    referel_id = models.CharField(max_length=20, unique=True, blank=True, null=True)  # now stored in DB

    def generate_referel_id(self):
        student_code = ''.join(filter(str.isalpha, self.student.name[:2].upper())) if self.student and hasattr(self.student, 'name') else "ST"
        guide_code = ''.join(filter(str.isalpha, self.guide.name[:1].upper())) if self.guide and hasattr(self.guide, 'name') else "G"
        alpha_part = (student_code + guide_code).ljust(3, 'X')  # Ensure 3-letter code

        hash_part = str(self.id % 10000).zfill(4) if self.id else "0000"
        return f"{alpha_part}-{hash_part}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save first to generate ID
        if not self.referel_id:
            self.referel_id = self.generate_referel_id()
            super().save(update_fields=['referel_id']) 
    # while saving if the link is changing from old to new then update it to Link model 
    # def save(self,*args,**kwargs):
    #     obj,created = Link.objects.get_or_create(project=self)
    #     print(self.pk,self.id)
    #     if self.id:
    #         pr = Project.objects.get(id=self.id)
    #         if self.file_link != pr.file_link:
    #             if obj:
    #                 obj.add(pr.file_link)
    #             else:
    #                 created.add(pr.file_link)
    #         else:
    #             print(self.link,pr.link)
    #             print("not changed")
    #     super().save(*args, **kwargs)
    
# class Link(models.Model):
#     links = models.JSONField(default=list)
#     project = models.OneToOneField(Project,on_delete=models.CASCADE)
    
#     def add(self,uri):
#         ls = self.links
#         ls.append({"link":uri,"at":str(datetime.now())})
#         self.links = ls
#         self.save()
        
#     def rem(self,idx):
#         ls = self.links
#         ls.pop(idx)
#         self.links = ls
#         self.save()
   
class PriorityType(models.IntegerChoices):
    FIRST = 1, 'First'
    SECOND = 2, 'Second'
    THIRD = 3, 'Third'
    FOURTH = 4, 'Fourth'
    FIFTH = 5, 'Fifth'

class StatusType(models.TextChoices):
    ACCEPTED = "ACCEPTED", "Accepted"
    REJECTED = "REJECTED", "Rejected"
    REMAINDERED = "REMAINDERED", "Reminder Sent"
    IDLE = "IDLE", "Idle"  # Next in line
    APPROACHED = "APPROACHED", "Approached"  # Initial mail sent but not reminded yet

class Evaluator(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    foreign_viva = models.BooleanField(default=False)
    phone = models.CharField(max_length=15)

    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    priority = models.IntegerField(choices=PriorityType.choices)
    last_sent_at = models.DateTimeField(null=True)
    status = models.CharField(
        max_length=15,
        choices=StatusType.choices,
        default=StatusType.IDLE
    )

    retry = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(3)]
    )

    is_viva = models.BooleanField(default=False)
    

    class Meta:
        unique_together = ('project', 'email')  # enforce 1 foreign + 1 non-foreign viva
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=['project', 'priority', 'foreign_viva'],
    #             name='unique_priority_per_project_foreign_flag'
    #         )
    #     ]

    def __str__(self):
        return f"{self.name} ({self.project.id})"

class Synopsis(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    file_link = models.CharField(max_length=200,null=False,blank=False)
    title  = models.CharField(max_length=200,null=False,blank=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    current = models.BooleanField(default=True)
    guide_approved = models.BooleanField(default=False)
    
    # before saving verify you having single current object enabled no two synopsis should be same 
    # for that get all the synopsis from this project and set it to false and then save the currrent one with true
    # def save():
