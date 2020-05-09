from django.db import models

# Create your models here.
class SubmittedCode(models.Model):
    userid = models.IntegerField() 
    questionnumber = models.IntegerField() 
    language = models.CharField(max_length=20)
    code = models.TextField(null=True)
    status = models.CharField(max_length=20)

class Case(models.Model):
    questionnumber = models.IntegerField() 
    sinput = models.TextField(null=True)
    answer = models.TextField(null=True)

class Question(models.Model):
    title = models.TextField(null=True)
    content = models.TextField(null=True)