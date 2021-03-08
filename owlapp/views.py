from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.shortcuts import redirect
import os
import subprocess
import logging
import json
from django.http import HttpResponse,Http404
import datetime
from threading import Timer
from owlapp.models import *
import owlapp.forms
from django.template.response import TemplateResponse
from django.http.response import JsonResponse
import time
import psutil
import resource
import os, os.path
import uuid
from django.contrib.auth.models import User
import re
from django.contrib.auth import authenticate, login as django_login
from . import views
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.contrib.auth import logout
import shutil
from pathlib import Path
import signal

def has_digit(text):
    if re.search("\d", text):
        return True
    return False


def has_alphabet(text):
    if re.search("[a-zA-Z]", text):
        return True
    return False

def logout_view(request):
    logout(request)
    return redirect('/')

def login_user(request):
    if request.method == 'POST':
        login_form =owlapp.forms.LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            django_login(request, user)
            return redirect('/')
        else:
            login_form.add_error(None, "ユーザー名またはパスワードが異なります。")
            return render(request, 'login.html', {'login_form': login_form})
        return render(request, 'login.html', {'login_form': login_form})
    else:
        login_form = owlapp.forms.LoginForm()
    return render(request, 'login.html', {'login_form': login_form})
    # アカウントとパスワードが合致したら、その人専用の投稿画面に遷移する
    # アカウントとパスワードが合致しなかったら、エラーメッセージ付きのログイン画面に遷移する


def registation_user(request):
    if request.method == 'POST':
        registration_form = owlapp.forms.RegistrationForm(request.POST)
        password = request.POST['password']
        if len(password) < 8:
            registration_form.add_error('password', "文字数が8文字未満です。")
        if not has_digit(password):
            registration_form.add_error('password', "数字が含まれていません")
        if not has_alphabet(password):
            registration_form.add_error('password', "アルファベットが含まれていません")
        if registration_form.has_error('password'):
            return render(request, 'registration.html', {'registration_form': registration_form})
        user = User.objects.create_user(username=request.POST['username'], password=password,
                                        email=request.POST['email'])
        return redirect('/login')
    else:
        registration_form = owlapp.forms.RegistrationForm()
    return render(request, 'registration.html', {'registration_form': registration_form})

def index(request):
    args = {}
    if request.user != None:
        args['currentuser'] = request.user.username
    return TemplateResponse(request, 'index.html', args)

def problems(request):
    args = {}
    if request.user != None:
        args['currentuser'] = request.user.username
    return TemplateResponse(request, 'problemlist.html',args)

def submissions(request):
    args = {}
    if request.user != None:
        args['currentuser'] = request.user.username
    args['submissions'] = SubmittedCode.objects.all().order_by('-judgeid')
    return TemplateResponse(request, 'submissions.html',args)


def problempage(request,id):
    obj = Question.objects.get(id = id)
    args = {}
    args['title'] = obj.title
    args['content'] = obj.content
    args['problemid'] = id
    if request.user != None:
        args['currentuser'] = request.user.username
    return TemplateResponse(request, 'problem.html',args)

def result(request,id):
    obj = SubmittedCode.objects.get(judgeid = id)
    args = {}
    args['id'] = str(id)
    args['language'] = obj.language
    args['problemnumber'] = str(obj.questionnumber)
    args['status'] = obj.status
    args['casenum'] = str(obj.casenum)
    args['ac'] = str(obj.ac)
    args['wa'] = str(obj.wa)
    args['tle'] = str(obj.tle)
    args['re'] = str(obj.re)
    args['code'] = obj.code.replace('\n','<br>')
    if request.user != None:
        args['currentuser'] = request.user.username
    return TemplateResponse(request, 'result.html',args)

lang = ["C","C++","Java","Python3","Ruby","Brainfuck"]
COMPILE_INDEX = 2
C_INDEX = 1
cmp = ["gcc","g++","javac"]
code = ["/main.c","/main.cpp","/Main.java","/main.py","/main.rb","/main.bf"]
execfile = ["/main","/main","/Main","/main.py","/main.rb","/main.bf"]

def subresults(request):
    kill = lambda process: process.kill()
    status = 'WJ'
    if request.method == 'POST':
        if request.user.username == "":
            return redirect('/login')
        error = ''
        process = ''
        os.makedirs("judge", exist_ok=True)
        folder = str(SubmittedCode.objects.all().count())
        i = 0
        for l in lang:
            if request.POST['language'] == l:
                os.mkdir("judge/" + folder)
                text_file = open("judge/" + folder+code[i], "w")
                text_file.write(request.POST["code"]) #コードをファイルに書き込む
                text_file.close()
                if i <= COMPILE_INDEX: #コンパイル型言語であるかどうかを判断する
                    bashCommand = ""
                    if i <= C_INDEX:
                        bashCommand = cmp[i]+" judge/"+folder+code[i]+" -o judge/"+folder+execfile[i]
                    else:
                        bashCommand = cmp[i]+" judge/" + folder+code[i]
                        logging.debug(bashCommand)
                    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                    output, error = process.communicate() #出力結果とエラー情報の取得
                    if 'error' in str(error):
                       status = 'CE'
                       dirpath = Path("judge", folder)
                       logging.debug(dirpath)
                       if dirpath.exists() and dirpath.is_dir():
                           shutil.rmtree(dirpath)
                break
            i+=1

    else:
        raise Http404
    obj = SubmittedCode.objects.create(judgeid=int(folder),language=request.POST['language'],userid = request.user.id,username = request.user.username,questionnumber=int(request.POST['problemid']),
    code = request.POST["code"],status = status,casenum = Case.objects.filter(questionnumber = int(request.POST['problemid'])).count(),
    ac = 0,wa = 0,tle = 0,re = 0)
    if status == 'WJ':
        return render(request, 'subresults.html',{
            'problemnumber':request.POST['problemid'],
            'status':"WJ...",
            'currentuser':request.user.username,
            'message':error,
            'number':Case.objects.filter(questionnumber = int(request.POST['problemid'])).count(),
            'range':range(Case.objects.filter(questionnumber = int(request.POST['problemid'])).count()),
            'id':folder,
            'initnumber':Case.objects.filter(questionnumber = int(request.POST['problemid']))[0].id,
            'language':request.POST['language']
        })
    else:
        return render(request, 'subresults.html',{
            'problemnumber':request.POST['problemid'],
            'status':"Compile Error!",
            'currentuser': request.user.username,
            'message':error.decode('UTF-8')
        })

execc1 = ["./codetest/","./codetest/","cd codetest/","python3 codetest/","ruby codetest/","bf codetest/"]
execc2 = ["/main","/main"," ; java Main","/main.py","/main.rb","/main.bf"]

TIMEOUT = 2.1*1000

def submit(request):
    if request.method == 'POST':
        kill = lambda process: process.kill()
        output = ''
        error = ''
        timeusage = None
        response = None
        memoryusage = 0
        os.makedirs("codetest", exist_ok=True)
        folder = str(len(os.listdir("codetest")))
        i = 0
        for l in lang:
            if request.POST['language'] == l:
                os.mkdir("codetest/" + folder)
                text_file = open("codetest/" + folder+code[i], "w")
                text_file.write(request.POST["code"]) #コードをファイルに書き込む
                text_file.close()
                if i <= COMPILE_INDEX: #コンパイル型言語であるかどうかを判断する
                    bashCommand = ""
                    if i <= C_INDEX:
                        bashCommand = cmp[i]+" codetest/"+folder+code[i]+" -o codetest/"+folder+execfile[i]
                    else:
                        bashCommand = cmp[i]+" codetest/" + folder+code[i]
                        logging.debug(bashCommand)
                    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                    output, error = process.communicate() #出力結果とエラー情報の取得
                    if 'error' in str(error):
                        dirpath = Path("codetest", folder)
                        if dirpath.exists() and dirpath.is_dir():
                            shutil.rmtree(dirpath)
                        response = json.dumps({'result':error.decode('UTF-8')})
                        return HttpResponse(response,content_type="text/javascript")
                bashCommand = execc1[i]+folder+execc2[i]
                process = psutil.Popen("exec " +bashCommand,shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                memoryusage = max(memoryusage, process.memory_info().rss / 1024 * 35)
                my_timer = Timer(2.1, process.kill)
                datetime1 = datetime.datetime.now().timestamp() * 1000
                datetime2 = 0
                memoryusage = 0
                try:
                    my_timer.start()
                    flag = False
                    while True:
                        memoryusage = max(memoryusage, process.memory_info().rss / 1024 * 35)
                        if flag == False:
                            output, error = process.communicate(input=request.POST['inputarea'].encode())
                            flag = True
                        retCode = process.poll()
                        if retCode is not None:
                            break
                finally:
                    my_timer.cancel()
                    datetime2 = datetime.datetime.now().timestamp() * 1000
                    logging.debug("fisnished")
                    if datetime2-datetime1>2.1*1000:
                        response = json.dumps({'result':'Time Limit Exceed!','timeusage':str(datetime2-datetime1),'memoryusage':str(memoryusage)})
                break
            i+=1
        dirpath = Path("codetest", folder)
        print(response)
        if dirpath.exists() and dirpath.is_dir():
            shutil.rmtree(dirpath)
        if process.returncode==0:
            response = json.dumps({'result':output.decode('UTF-8'),'timeusage':str(datetime2-datetime1),'memoryusage':str(memoryusage)})
        elif response==None:
            logging.debug(error)
            response = json.dumps({'result':'Runtime Error! Error Code:'+str(process.returncode),'timeusage':str(datetime2-datetime1),'memoryusage':str(memoryusage)})
        return HttpResponse(response,content_type="text/javascript")
    else:
        raise Http404

exec1 = ["./judge/","./judge/","cd judge/","python3 judge/","ruby judge/","bf judge/"]
exec2 = ["/main","/main"," ; java Main","/main.py","/main.rb","/main.bf"]

def judge(request):
    kill = lambda process: process.kill()
    process = None
    status = 'WJ...'
    output = ''
    error = ''
    case = Case.objects.filter(questionnumber = int(request.GET.get('problemid', None)))[int(request.GET.get('casenumber', None))]
    datetime1 = 0
    datetime2 = 0
    memoryusage = 0
    i = 0
    for l in lang:
        if request.GET.get('language', None) == l:
            bashCommand = exec1[i]+request.GET.get('submissionid', None)+exec2[i]
            process = psutil.Popen("exec " +bashCommand,shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            break
        i+=1
    memoryusage = max(memoryusage, process.memory_info().rss / 1024 * 35)
    datetime1 = datetime.datetime.now().timestamp() * 1000
    my_timer = Timer(2.1, process.kill)
    try:
        my_timer.start()
        flag = False
        while True:
            memoryusage = max(memoryusage, process.memory_info().rss / 1024 * 35)
            logging.debug(case.sinput)
            if flag == False:
                output, error = process.communicate(case.sinput.encode())
                flag = True
            retCode = process.poll()
            if retCode is not None:
                break
    finally:
        my_timer.cancel()
        datetime2 = datetime.datetime.now().timestamp() * 1000
    data = SubmittedCode.objects.filter(judgeid = request.GET.get('submissionid', None))[0]
    if datetime2-datetime1>2.1*1000:
        status = 'TLE'
        data.tle+=1
        data.status = 'TLE'
    elif process.returncode != 0:
        status = 'RE'
        logging.debug(error)
        data.re += 1
        data.status = 'RE'
    elif output.decode('UTF-8') == case.answer+"\n":
        status = 'AC'
        data.ac += 1
    else:
        status = 'WA'
        data.wa += 1
        data.status = 'WA'
    if data.ac == data.casenum:
        data.status = "AC"
    data.save()
    if data.ac + data.wa + data.tle + data.re == data.casenum:
        dirpath = Path("judge", request.GET.get('submissionid', None))
        logging.debug(dirpath)
        if dirpath.exists() and dirpath.is_dir():
            shutil.rmtree(dirpath) #実行ファイルを削除する
    if data.ac == data.casenum:
        params = {"result":status,"timeusage":str(datetime2-datetime1),"memoryusage":str(memoryusage),"ac":"true"}
    else:
        params = {"result":status,"timeusage":str(datetime2-datetime1),"memoryusage":str(memoryusage),"ac":"false"}
    json_str = json.dumps(params, ensure_ascii=False, indent=2)
    return HttpResponse(json_str)
