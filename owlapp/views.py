from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
import os
import subprocess
import logging
import json
from django.http import HttpResponse,Http404
import datetime
from threading import Timer
from owlapp.models import *
from django.template.response import TemplateResponse
from django.http.response import JsonResponse

def index(request):
    return render(request, 'index.html')

def problems(request):
    obj = Question.objects.get(id = 1)
    args = {}
    args['title'] = obj.title
    args['content'] = obj.content
    return TemplateResponse(request, 'problem.html',args)

def subresults(request):
    ill = lambda process: process.kill()
    status = 'WJ'
    if request.method == 'POST':
        error = ''
        process = ''
        if request.POST['language'] == 'C':
            text_file = open("judge/main.c", "w")
            text_file.write(request.POST["code"])
            text_file.close()
            bashCommand = "gcc judge/main.c -o judge/main"
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            output, error = process.communicate()
            if 'error' in str(error):
               status = 'CE'
              
        elif request.POST['language'] == 'C++':
            text_file = open("judge/main.cpp", "w")
            text_file.write(request.POST["code"])
            text_file.close()
            bashCommand = "g++ judge/main.cpp -o judge/main"
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            output, error = process.communicate()
            if 'error' in str(error):
               status = 'CE'
        elif request.POST['language'] == 'Java':
            text_file = open("judge/main.cpp", "w")
            text_file.write(request.POST["code"])
            text_file.close()
            bashCommand = "g++ judge/main.cpp -o judge/main"
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            output, error = process.communicate()
            if 'error' in str(error):
               status = 'CE'
        elif request.POST['language'] == 'Python3':
            text_file = open("judge/main.py", "w")
            text_file.write(request.POST["code"])
            text_file.close()
            
    else:
        raise Http404
    if status == 'WJ':
        return render(request, 'subresults.html',{
            'problemnumber':'1',
            'status':"WJ...",
            'message':error.decode('UTF-8'),
            'number':Case.objects.filter(questionnumber = 1).count(),
            'range':range(Case.objects.filter(questionnumber = 1).count())
        })
    else:
        return render(request, 'subresults.html',{
            'problemnumber':'1',
            'status':"Compile Error!",
            'message':error.decode('UTF-8')
        })

def submit(request):
    kill = lambda process: process.kill()
    if request.method == 'POST':
        output = ''
        error = ''
        process = ''
        timeusage = None
        if request.POST['language'] == 'C':
            text_file = open("judge/main.c", "w")
            text_file.write(request.POST["code"])
            text_file.close()
            bashCommand = "gcc judge/main.c -o judge/main"
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            output, error = process.communicate()
            if 'error' in str(error):
                response = json.dumps({'result':error.decode('UTF-8')})
                return HttpResponse(response,content_type="text/javascript")
            else:
                error = None
                bashCommand = "./judge/main"
                datetime1 = datetime.datetime.now().timestamp() * 1000
                process = subprocess.Popen(bashCommand.split(), stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                my_timer = Timer(2.1, kill, [process])
                try:
                    my_timer.start()
                    output, error = process.communicate(input=request.POST['inputarea'].encode())
                finally:
                    my_timer.cancel()
                datetime2 = datetime.datetime.now().timestamp() * 1000
                logging.debug(datetime2-datetime1)
                if datetime2-datetime1>2.1*1000:
                    response = json.dumps({'result':'Time Limit Exceed!','timeusage':str(datetime2-datetime1)})
                    return HttpResponse(response,content_type="text/javascript")
                
                

        elif request.POST['language'] == 'C++':
            text_file = open("judge/main.cpp", "w")
            text_file.write(request.POST["code"])
            text_file.close()
            bashCommand = "g++ judge/main.cpp -o judge/main"
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            output, error = process.communicate()
            if 'error' in str(error):
                response = json.dumps({'result':error.decode('UTF-8')})
                return HttpResponse(response,content_type="text/javascript")
            else:
                bashCommand = "./judge/main"
                datetime1 = datetime.datetime.now().timestamp() * 1000
                process = subprocess.Popen(bashCommand.split(), stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                my_timer = Timer(2.1, kill, [process])
                try:
                    my_timer.start()
                    output, error = process.communicate(input=request.POST['inputarea'].encode())
                finally:
                    my_timer.cancel()
                datetime2 = datetime.datetime.now().timestamp() * 1000
                logging.debug(datetime2-datetime1)
                if datetime2-datetime1>2.1*1000:
                    response = json.dumps({'result':'Time Limit Exceed!','timeusage':str(datetime2-datetime1)})
                    return HttpResponse(response,content_type="text/javascript")
        elif request.POST['language'] == 'Java':
            text_file = open("judge/main.cpp", "w")
            text_file.write(request.POST["code"])
            text_file.close()
            bashCommand = "g++ judge/main.cpp -o judge/main"
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            output, error = process.communicate()
            if 'error' in str(error):
                response = json.dumps({'result':error.decode('UTF-8')})
                return HttpResponse(response,content_type="text/javascript")
            else:
                bashCommand = "./judge/main"
                datetime1 = datetime.datetime.now().timestamp() * 1000
                process = subprocess.Popen(bashCommand.split(), stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                my_timer = Timer(2.1, kill, [process])
                try:
                    my_timer.start()
                    output, error = process.communicate(input=request.POST['inputarea'].encode())
                finally:
                    my_timer.cancel()
                datetime2 = datetime.datetime.now().timestamp() * 1000
                logging.debug(datetime2-datetime1)
                if datetime2-datetime1>2.1*1000:
                    response = json.dumps({'result':'Time Limit Exceed!','timeusage':str(datetime2-datetime1)})
                    return HttpResponse(response,content_type="text/javascript")
        elif request.POST['language'] == 'Python3':
            text_file = open("judge/main.py", "w")
            text_file.write(request.POST["code"])
            text_file.close()
            bashCommand = "python3 judge/main.py"
            datetime1 = datetime.datetime.now().timestamp() * 1000
            process = subprocess.Popen(bashCommand.split(), stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            my_timer = Timer(2.1, kill, [process])
            try:
                my_timer.start()
                output, error = process.communicate(input=request.POST['inputarea'].encode())
            finally:
                my_timer.cancel()
                datetime2 = datetime.datetime.now().timestamp() * 1000
                logging.debug(datetime2-datetime1)
            if datetime2-datetime1>2.1*1000:
                response = json.dumps({'result':'Time Limit Exceed!','timeusage':str(datetime2-datetime1)})
                return HttpResponse(response,content_type="text/javascript")
        if(process.returncode==0):
            response = json.dumps({'result':output.decode('UTF-8'),'timeusage':str(datetime2-datetime1)})
            return HttpResponse(response,content_type="text/javascript")
        else:
            response = json.dumps({'result':'Runtime Error! Error Code:'+str(process.returncode),'timeusage':str(datetime2-datetime1)})
            return HttpResponse(response,content_type="text/javascript")
    else:
        raise Http404

def judge(request):
    kill = lambda process: process.kill()
    status = 'WJ...'
    output = ''
    case = Case.objects.filter(questionnumber = int(request.GET.get('problemid', None)))[int(request.GET.get('casenumber', None))]
    bashCommand = "./judge/main"
    datetime1 = datetime.datetime.now().timestamp() * 1000
    datetime2 = 0
    process = subprocess.Popen(bashCommand.split(), stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    my_timer = Timer(2.1, kill, [process])
    try:
        my_timer.start()
        output, error = process.communicate(input=case.sinput.encode())
    finally:
        my_timer.cancel()
        datetime2 = datetime.datetime.now().timestamp() * 1000
    if datetime2-datetime1>2.1*1000:
        status = 'TLE'
    elif process.returncode != 0:
        status = 'RE'
    elif output.decode('UTF-8') == case.answer:
        status = 'AC'
    else:
        status = 'WA'
    params = {"result":status,"timeusage":str(datetime2-datetime1),}
    json_str = json.dumps(params, ensure_ascii=False, indent=2) 
    return HttpResponse(json_str)

def submissions(request):
    return render(request, 'submissions.html')
