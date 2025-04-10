from django.contrib import admin
from .models import *

admin.site.register(Mail)
admin.site.register(Reply)
admin.site.register(MailLog)