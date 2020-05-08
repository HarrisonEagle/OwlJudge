from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
import os
import subprocess
import logging
import json
from django.http import HttpResponse,Http404

def index(request):
    return render(request, 'index.html')

def submit(request):
    if request.method == 'POST':
        output = ''
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
                response = json.dumps({'result':error.decode('UTF-8')})
                return HttpResponse(response,content_type="text/javascript")
            else:
                error = None
                bashCommand = "./judge/main"
                process = subprocess.Popen(bashCommand.split(), stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                output, error = process.communicate(input=request.POST['inputarea'].encode())
                

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
                process = subprocess.Popen(bashCommand.split(), stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                output, error = process.communicate(input=request.POST['inputarea'].encode())
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
                process = subprocess.Popen(bashCommand.split(), stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                output, error = process.communicate(input=request.POST['inputarea'].encode())
        elif request.POST['language'] == 'Python3':
            text_file = open("judge/main.py", "w")
            text_file.write(request.POST["code"])
            text_file.close()
            bashCommand = "python3 judge/main.py"
            process = subprocess.Popen(bashCommand.split(), stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            output, error = process.communicate(input=request.POST['inputarea'].encode())
        if(process.returncode==0):
            response = json.dumps({'result':output.decode('UTF-8')})
            return HttpResponse(response,content_type="text/javascript")
        else:
            response = json.dumps({'result':'Runtime Error! Error Code:'+str(process.returncode)})
            return HttpResponse(response,content_type="text/javascript")
    else:
        raise Http404
