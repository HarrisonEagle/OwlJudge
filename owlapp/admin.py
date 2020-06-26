from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.SubmittedCode)
admin.site.register(models.Case)
admin.site.register(models.Question)
