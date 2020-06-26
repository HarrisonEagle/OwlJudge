from django.db import models



# Create your models here.
class SubmittedCode(models.Model):
    judgeid = models.IntegerField()
    userid = models.IntegerField()
    questionnumber = models.IntegerField()
    username = models.TextField(null=True)
    language = models.CharField(max_length=20)
    code = models.TextField(null=True)
    status = models.CharField(max_length=20)
    casenum = models.IntegerField()
    ac = models.IntegerField()
    wa = models.IntegerField()
    tle = models.IntegerField()
    re = models.IntegerField()


class Case(models.Model):
    questionnumber = models.IntegerField() 
    sinput = models.TextField(null=True)
    answer = models.TextField(null=True)

class Question(models.Model):
    title = models.TextField(null=True)
    content = models.TextField(null=True)
