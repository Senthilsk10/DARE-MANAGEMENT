from django.db import models
from projects.models import Project,Evaluator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Mail(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    to = models.ForeignKey(Evaluator, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)
    subject = models.TextField(null=False,default="Not Mentioned")
    message_id = models.CharField(max_length=40,null=False)
    
    def __str__(self):
        return f"{self.content}"

class Response(models.Model):
    mail = models.ForeignKey(Mail, on_delete=models.CASCADE) # reply mail linking (work on what if we dont get mail and the user initiated it first)
    evaluator = models.ForeignKey(Evaluator, on_delete=models.CASCADE)
    response = models.TextField() # if subject is modify then get the required modfication, and file link from the repsonse using parse_function 
    attachments = models.JSONField(help_text="Attachment URLs stored as JSON list",default=list)
    subject = models.TextField(null=False,default="Not Mentioned") # handle this in uploading read emails from gsheets aasit raises not null constraint (if email does not have subject then it was not our predifined version)
    message_id = models.CharField(max_length=40,null=False)
    
    # to Implement : 
    # a function that uses subject and response to parse the required data from the mail
    def parse_response(self):
        pass
    
    def __str__(self):
        return f"{self.response}"

class MailType(models.TextChoices):
    APPROACH = 'Approach', 'Approach Email to viva coordinators'
    REMINDER = 'Reminder', 'Reminder for pending mail'
    ACCEPTED = 'Accepted', 'Mail received for acceptance of project'
    REJECTED = 'Rejected', 'Mail received for project rejection'
    MODIFICATIONS = 'Modifications', 'Mail about project modifications'

class MailLog(models.Model):
    type = models.CharField(max_length=20, choices=MailType.choices)

    # ContentType Fields for Generic Relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_type_display()} - {self.content_object}"
    
    #implement get absolute url pointing towards the recieved mail -> content_object.id wth mail viewer or some thing