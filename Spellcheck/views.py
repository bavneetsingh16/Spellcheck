from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str
from wsgiref.util import FileWrapper
#from Spellcheck.SpellChecker import *
import Spellcheck.SpellChecker as sc
import os

file_name=""
input_folder='Spellcheck/UploadFiles/'
output_folder= 'Spellcheck/Correctfiles/'
# Create your views here.
#@csrf_exempt
def index(request):
	global input_folder,output_folder
	for the_file in os.listdir(input_folder):
	    file_path = os.path.join(input_folder, the_file)
	    try:
	        if os.path.isfile(file_path):
	            os.unlink(file_path)
	        #elif os.path.isdir(file_path): shutil.rmtree(file_path)
	    except Exception as e:
	        print(e)
	for the_file in os.listdir(output_folder):
	    file_path = os.path.join(output_folder, the_file)
	    try:
	        if os.path.isfile(file_path):
	            os.unlink(file_path)
	        #elif os.path.isdir(file_path): shutil.rmtree(file_path)
	    except Exception as e:
	        print(e)

	return render(request,"upload.html")
	#return HttpResponse("Hello, world. You're at the polls index.")

#@csrf_exempt
def upload(request):
	global file_name,input_folder
	myfile = request.FILES['file']
	file_name=myfile.name
	loc=input_folder+str(myfile.name)
	#session_filename = request.session.get('num')
	#request.session['session_filename'] = file_name
	fs = FileSystemStorage(location='Spellcheck/UploadFiles/')
	filename = fs.save(myfile.name, myfile)
	sc.run(loc,str(myfile.name))

	return render(request,"download.html")

#@csrf_exempt
def download(request):
	global file_name,output_folder
	filename=file_name
	#filename=str(request.session.get('session_filename'))
	#path = 'Spellcheck/Correctfiles/'
	#output_folder=path+filename
	f = open(output_folder+filename, "r")
	response = HttpResponse(FileWrapper(f), content_type='application/txt')
	response['Content-Disposition'] = 'attachment; filename='+filename
	f.close()
	return response
