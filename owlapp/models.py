from django.db import models

class SubmittedCode(models.Model):#ユーザーが提出したコード
    judgeid = models.IntegerField(primary_key=True)
    userid = models.IntegerField()
    questionnumber = models.IntegerField()
    username = models.TextField(null=True)
    language = models.CharField(max_length=20)#提出言語
    code = models.TextField(null=True)#コード
    status = models.CharField(max_length=20)#ステータス
    casenum = models.IntegerField()
    ac = models.IntegerField()
    wa = models.IntegerField()
    tle = models.IntegerField()
    re = models.IntegerField()


class Case(models.Model):
    id = models.IntegerField(primary_key=True)
    questionnumber = models.IntegerField()
    sinput = models.TextField(null=True)#入力
    answer = models.TextField(null=True)#答え

class Question(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.TextField(null=True)
    content = models.TextField(null=True)
