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
    return redirect('/owlapp')

def login_user(request):
    if request.method == 'POST':
        login_form =owlapp.forms.LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            django_login(request, user)
            return redirect('/owlapp')
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
        return redirect('/owlapp/login')
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
    args['submissions'] = SubmittedCode.objects.all().order_by('-id')
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

def subresults(request):
    kill = lambda process: process.kill()
    status = 'WJ'
    if request.method == 'POST':
        if request.user.username == "":
            return redirect('/owlapp/login')
        error = ''
        process = ''
        folder = str(len(os.listdir("judge")))
        logging.debug(folder)
        if request.POST['language'] == 'C':
            os.mkdir("judge/" + folder)
            text_file = open("judge/" + folder+"/main.c", "w")
            text_file.write(request.POST["code"])
            text_file.close()
            bashCommand = "gcc judge/"+folder+"/main.c -o judge/"+folder+"/main"
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            output, error = process.communicate()
            if 'error' in str(error):
               status = 'CE'
              
        elif request.POST['language'] == 'C++':
            os.mkdir("judge/" + folder)
            text_file = open("judge/" + folder+"/main.cpp", "w")
            text_file.write(request.POST["code"])
            text_file.close()
            bashCommand = "g++ judge/" + folder+"/main.cpp -o judge/"+folder+"/main"
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            output, error = process.communicate()
            if 'error' in str(error):
               status = 'CE'
        elif request.POST['language'] == 'Java':
            os.mkdir("judge/" + folder)
            text_file = open("judge/" + folder+"/Main.java", "w")
            text_file.write(request.POST["code"])
            text_file.close()
            bashCommand = "javac judge/" + folder+"/Main.java"
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            output, error = process.communicate()
            if 'error' in str(error):
               status = 'CE'
        elif request.POST['language'] == 'Python3':
            os.mkdir("judge/" + folder)
            text_file = open("judge/" + folder+"/main.py", "w")
            text_file.write(request.POST["code"])
            text_file.close()
        elif request.POST['language'] == 'Ruby':
            os.mkdir("judge/" + folder)
            text_file = open("judge/"+ folder+"/main.rb", "w")
            text_file.write(request.POST["code"])
            text_file.close()
        elif request.POST['language'] == 'Brainfuck':
            os.mkdir("judge/" + folder)
            text_file = open("judge/" + folder+"/main.bf", "w")
            text_file.write(request.POST["code"])
            text_file.close()
            
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

def submit(request):
    if request.method == 'POST':
        output = ''
        error = ''
        process = ''
        timeusage = None
        memoryusage = 0
        folder = str(len(os.listdir("codetest")))
        logging.debug(folder)
        if request.POST['language'] == 'C':
            os.mkdir("codetest/" + folder)
            text_file = open("codetest/"+folder+"/main.c", "w")
            text_file.write(request.POST["code"])
            text_file.close()
            command = "gcc codetest/"+folder+"/main.c -o codetest/"+folder+"/main"
            process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output,error = process.communicate()
            if 'error' in str(error):
                response = json.dumps({'result':error.decode('UTF-8')})
                return HttpResponse(response,content_type="text/javascript")
            else:
                error = None
                datetime1 = datetime.datetime.now().timestamp() * 1000
                command = "./codetest/"+folder+"/main"
                process = psutil.Popen(command.split(), shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                memoryusage = max(memoryusage,process.memory_info().rss/1024)
                logging.debug("memory"+str(memoryusage))
                my_timer = Timer(2.1, process.kill)
                try:
                    my_timer.start()
                    flag = False
                    while True:
                        memoryusage = max(memoryusage, process.memory_info().rss / 1024)
                        logging.debug("memory" + str(memoryusage))
                        if flag == False:
                            output, error = process.communicate(input=request.POST['inputarea'].encode())
                            flag = True
                        retCode = process.poll()
                        if retCode is not None:
                            break
                finally:
                    my_timer.cancel()
                datetime2 = datetime.datetime.now().timestamp() * 1000
                logging.debug(datetime2-datetime1)
                if datetime2-datetime1>2.1*1000:
                    response = json.dumps({'result':'Time Limit Exceed!','timeusage':str(datetime2-datetime1),'memoryusage':str(memoryusage)})
                    return HttpResponse(response,content_type="text/javascript")

        elif request.POST['language'] == 'C++':
            os.mkdir("codetest/" + folder)
            text_file = open("codetest/" + folder + "/main.cpp", "w")
            text_file.write(request.POST["code"])
            text_file.close()
            command = "g++ codetest/" + folder + "/main.cpp -o codetest/" + folder + "/main"
            process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = process.communicate()
            if 'error' in str(error):
                response = json.dumps({'result': error.decode('UTF-8')})
                return HttpResponse(response, content_type="text/javascript")
            else:
                error = None
                datetime1 = datetime.datetime.now().timestamp() * 1000
                command = "./codetest/" +  folder + "/main"
                process = psutil.Popen(command.split(), shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                memoryusage = max(memoryusage, process.memory_info().rss / 1024)
                logging.debug("memory" + str(memoryusage))
                my_timer = Timer(2.1, process.kill)
                try:
                    my_timer.start()
                    flag = False
                    while True:
                        memoryusage = max(memoryusage, process.memory_info().rss / 1024)
                        logging.debug("memory" + str(memoryusage))
                        if flag == False:
                            output, error = process.communicate(input=request.POST['inputarea'].encode())
                            flag = True
                        retCode = process.poll()
                        if retCode is not None:
                            break
                finally:
                    my_timer.cancel()
                datetime2 = datetime.datetime.now().timestamp() * 1000
                logging.debug(datetime2 - datetime1)
                if datetime2 - datetime1 > 2.1 * 1000:
                    response = json.dumps({'result': 'Time Limit Exceed!', 'timeusage': str(datetime2 - datetime1),
                                           'memoryusage': str(memoryusage)})
                    return HttpResponse(response, content_type="text/javascript")
        elif request.POST['language'] == 'Java':
            os.mkdir("codetest/" + folder)
            text_file = open("codetest/" + folder + "/Main.java", "w")
            text_file.write(request.POST["code"])
            text_file.close()
            command = "javac codetest/" + folder + "/Main.java"
            process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = process.communicate()
            if 'error' in str(error):
                response = json.dumps({'result': error.decode('UTF-8')})
                return HttpResponse(response, content_type="text/javascript")
            else:
                error = None
                datetime1 = datetime.datetime.now().timestamp() * 1000
                cmd1 = "cd codetest/" + folder
                cmd2 = "java Main"
                process = psutil.Popen("{}; {}".format(cmd1, cmd2), shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
                memoryusage = max(memoryusage, process.memory_info().rss / 1024*13)
                logging.debug("memory" + str(memoryusage))
                my_timer = Timer(2.1, process.kill)
                try:
                    my_timer.start()
                    flag = False
                    while True:
                        memoryusage = max(memoryusage, process.memory_info().rss / 1024*13)
                        logging.debug("memory" + str(memoryusage))
                        if flag == False:
                            output, error = process.communicate(input=request.POST['inputarea'].encode())
                            flag = True
                        retCode = process.poll()
                        if retCode is not None:
                            break
                finally:
                    my_timer.cancel()
                datetime2 = datetime.datetime.now().timestamp() * 1000
                logging.debug(datetime2 - datetime1)
                if datetime2 - datetime1 > 2.1 * 1000:
                    response = json.dumps({'result': 'Time Limit Exceed!', 'timeusage': str(datetime2 - datetime1),'memoryusage': str(memoryusage)})
                    return HttpResponse(response, content_type="text/javascript")
        elif request.POST['language'] == 'Python3':
            os.mkdir("codetest/" + folder)
            text_file = open("codetest/" + folder + "/main.py", "w")
            text_file.write(request.POST["code"])
            text_file.close()
            datetime1 = datetime.datetime.now().timestamp() * 1000
            command = "python3 codetest/" +  folder + "/main.py"
            process = psutil.Popen(command.split(),stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            memoryusage = max(memoryusage, process.memory_info().rss / 1024*10)
            logging.debug("memory" + str(memoryusage))
            my_timer = Timer(2.1, process.kill)
            try:
                my_timer.start()
                flag = False
                while True:
                    memoryusage = max(memoryusage, process.memory_info().rss / 1024*10)
                    logging.debug("memory" + str(memoryusage))
                    if flag==False:
                        output, error = process.communicate(input=request.POST['inputarea'].encode())
                        flag = True
                    retCode = process.poll()
                    if retCode is not None:
                        break
            finally:
                my_timer.cancel()
            datetime2 = datetime.datetime.now().timestamp() * 1000
            logging.debug(datetime2 - datetime1)
            if datetime2 - datetime1 > 3.0 * 1000:
                response = json.dumps({'result': 'Time Limit Exceed!', 'timeusage': str(datetime2 - datetime1),
                                       'memoryusage': str(memoryusage)})
                return HttpResponse(response, content_type="text/javascript")
        elif request.POST['language'] == 'Ruby':
            os.mkdir("codetest/" + folder)
            text_file = open("codetest/" + folder + "/main.rb", "w")
            text_file.write(request.POST["code"])
            text_file.close()
            datetime1 = datetime.datetime.now().timestamp() * 1000
            command = "ruby codetest/" +  folder + "/main.rb"
            process = psutil.Popen(command.split(),stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            memoryusage = max(memoryusage, process.memory_info().rss / 1024*35)
            logging.debug("memory" + str(memoryusage))
            my_timer = Timer(2.1, process.kill)
            try:
                my_timer.start()
                flag = False
                while True:
                    memoryusage = max(memoryusage, process.memory_info().rss / 1024*35)
                    logging.debug("memory" + str(memoryusage))
                    if flag==False:
                        output, error = process.communicate(input=request.POST['inputarea'].encode())
                        flag = True
                    retCode = process.poll()
                    if retCode is not None:
                        break
            finally:
                my_timer.cancel()
            datetime2 = datetime.datetime.now().timestamp() * 1000
            logging.debug(datetime2 - datetime1)
            if datetime2 - datetime1 > 3.0 * 1000:
                response = json.dumps({'result': 'Time Limit Exceed!', 'timeusage': str(datetime2 - datetime1),
                                       'memoryusage': str(memoryusage)})
                return HttpResponse(response, content_type="text/javascript")
        elif request.POST['language'] == 'Brainfuck':
            os.mkdir("codetest/" + folder)
            text_file = open("codetest/" + folder + "/main.bf", "w")
            text_file.write(request.POST["code"])
            text_file.close()
            datetime1 = datetime.datetime.now().timestamp() * 1000
            command = "bf codetest/" +  folder + "/main.bf"
            process = psutil.Popen(command.split(),stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            memoryusage = max(memoryusage, process.memory_info().rss / 1024)
            logging.debug("memory" + str(memoryusage))
            my_timer = Timer(2.1, process.kill)
            try:
                my_timer.start()
                flag = False
                while True:
                    memoryusage = max(memoryusage, process.memory_info().rss / 1024)
                    logging.debug("memory" + str(memoryusage))
                    if flag==False:
                        output, error = process.communicate(input=request.POST['inputarea'].encode())
                        flag = True
                    retCode = process.poll()
                    if retCode is not None:
                        break
            finally:
                my_timer.cancel()
            datetime2 = datetime.datetime.now().timestamp() * 1000
            logging.debug(datetime2 - datetime1)
            if datetime2 - datetime1 > 3.0 * 1000:
                response = json.dumps({'result': 'Time Limit Exceed!', 'timeusage': str(datetime2 - datetime1),
                                       'memoryusage': str(memoryusage)})
                return HttpResponse(response, content_type="text/javascript")
        if(process.returncode==0):
            response = json.dumps({'result':output.decode('UTF-8'),'timeusage':str(datetime2-datetime1),'memoryusage':str(memoryusage)})
            return HttpResponse(response,content_type="text/javascript")
        else:
            logging.debug(error)
            response = json.dumps({'result':'Runtime Error! Error Code:'+str(process.returncode),'timeusage':str(datetime2-datetime1),'memoryusage':str(memoryusage)})
            return HttpResponse(response,content_type="text/javascript")
    else:
        raise Http404

def judge(request):
    kill = lambda process: process.kill()
    status = 'WJ...'
    output = ''
    case = Case.objects.filter(questionnumber = int(request.GET.get('problemid', None)))[int(request.GET.get('casenumber', None))]
    datetime1 = datetime.datetime.now().timestamp() * 1000
    datetime2 = 0
    memoryusage = 0
    if request.GET.get('language', None) == 'C':
        bashCommand = "./judge/"+request.GET.get('submissionid', None)+"/main"
        process = psutil.Popen(bashCommand.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
    elif request.GET.get('language', None) == 'C++':
        bashCommand = "./judge/"+request.GET.get('submissionid', None)+"/main"
        process = psutil.Popen(bashCommand.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
    elif request.GET.get('language', None) == 'Java':
        bashCommand = "java judge/"+request.GET.get('submissionid', None)+"/Main.java"
        process = psutil.Popen(bashCommand.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
    elif request.GET.get('language', None) == 'Python3':
        bashCommand = "python3 judge/"+request.GET.get('submissionid', None)+"/main.py"
        process = psutil.Popen(bashCommand.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
    elif request.GET.get('language', None) == 'Ruby':
        bashCommand = "ruby judge/"+request.GET.get('submissionid', None)+"/main.rb"
        process = psutil.Popen(bashCommand.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
    elif request.GET.get('language', None) == 'Brainfuck':
        bashCommand = "bf judge/"+request.GET.get('submissionid', None)+"/main.bf"
        process = psutil.Popen(bashCommand.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

    memoryusage = max(memoryusage, process.memory_info().rss / 1024 * 35)
    logging.debug("memory" + str(memoryusage))
    my_timer = Timer(2.1, process.kill)
    try:
        my_timer.start()
        flag = False
        while True:
            memoryusage = max(memoryusage, process.memory_info().rss / 1024 * 35)
            logging.debug("memory" + str(memoryusage))
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
    if data.ac == data.casenum:
        params = {"result":status,"timeusage":str(datetime2-datetime1),"memoryusage":str(memoryusage),"ac":"true"}
    else:
        params = {"result":status,"timeusage":str(datetime2-datetime1),"memoryusage":str(memoryusage),"ac":"false"}
    json_str = json.dumps(params, ensure_ascii=False, indent=2) 
    return HttpResponse(json_str)
