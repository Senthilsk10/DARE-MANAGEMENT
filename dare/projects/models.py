from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from students.models import Student,Guide
from datetime import datetime

class Project(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE)
    title  = models.CharField(max_length=200,null=False,blank=False)
    file_link = models.CharField(max_length=200,null=True,blank=True)
    uploaded_at = models.DateTimeField( auto_now_add=True)
    current = models.BooleanField(default=True)
    guide_approved = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)
    
    # while saving if the link is changing from old to new then update it to Link model 
    def save(self,*args,**kwargs):
        obj,created = Link.objects.get_or_create(project=self)
        print(self.pk,self.id)
        if self.id:
            pr = Project.objects.get(id=self.id)
            if self.file_link != pr.file_link:
                if obj:
                    obj.add(pr.file_link)
                else:
                    created.add(pr.file_link)
            else:
                print(self.link,pr.link)
                print("not changed")
        super().save(*args, **kwargs)
    
class Link(models.Model):
    links = models.JSONField(default=list)
    project = models.OneToOneField(Project,on_delete=models.CASCADE)
    
    def add(self,uri):
        ls = self.links
        ls.append({"link":uri,"at":str(datetime.now())})
        self.links = ls
        self.save()
        
    def rem(self,idx):
        ls = self.links
        ls.pop(idx)
        self.links = ls
        self.save()
        
class Evaluator(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    foreign_viva = models.BooleanField(default=False)
    phone = models.CharField(max_length=15, unique=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    
class Viva(models.Model):
    viva_1 = models.ForeignKey(Evaluator, on_delete=models.SET_NULL, null=True, related_name="viva_1_projects",default=1)
    viva_2 = models.ForeignKey(Evaluator, on_delete=models.SET_NULL, null=True, related_name="viva_2_projects",default=2)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

class Synopsis(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    file_link = models.CharField(max_length=200,null=False,blank=False)
    title  = models.CharField(max_length=200,null=False,blank=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    current = models.BooleanField(default=True)
    guide_approved = models.BooleanField(default=False)
