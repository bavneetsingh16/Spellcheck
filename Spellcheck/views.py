from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str
from wsgiref.util import FileWrapper
import Spellcheck.SpellChecker as sc
import os
import boto3
from boto3.dynamodb.types import Binary
from dynamodb_encryption_sdk.encrypted.table import EncryptedTable
from dynamodb_encryption_sdk.identifiers import CryptoAction
from dynamodb_encryption_sdk.material_providers.aws_kms import AwsKmsCryptographicMaterialsProvider
from dynamodb_encryption_sdk.structures import AttributeActions

file_name=""
input_folder='Spellcheck/UploadFiles/'
output_folder= 'Spellcheck/Correctfiles/'
# Create your views here.


def signup_login(request):
    if request.method == 'GET':
        return render(request,'index.html')
    if request.method == 'POST':
    	 dynamodb = boto3.resource('dynamodb',region_name='us-east-1')
    	 table = dynamodb.Table('users')
    	 aws_cmk_id=''
    	 aws_kms_cmp=AwsKmsCryptographicMaterialsProvider(key_id=aws_cmk_id)
    	 name2 = request.POST['login']
    	 name3=str(name2)
    	 actions = AttributeActions(
				    #default_action=CryptoAction.ENCRYPT_AND_SIGN,
				    default_action=CryptoAction.DO_NOTHING,
				    attribute_actions={
				    	'userid': CryptoAction.DO_NOTHING,
				        'first_name': CryptoAction.DO_NOTHING,
				        'last_name': CryptoAction.DO_NOTHING,
				        'password':CryptoAction.ENCRYPT_AND_SIGN
				        
				    }
				  )
    	 encrypted_table = EncryptedTable(
					    table=table,
					    materials_provider=aws_kms_cmp,
					    attribute_actions=actions
					)
    	 #signup='signup'
    	 #login='login'
    	 print("check*****",name2)
    	 if(name2=='send'):
    	 	 return render(request,"upload.html")
    	 if(name2=='signup'):
             	first_name=request.POST.get('first','')
             	last_name=request.POST.get('last','')
             	email = request.POST.get('newemail','')
             	password = request.POST.get('newpassword','')
             	print ("first name is ", first_name, "last name is ", last_name)
             	encrypted_table.put_item(Item={
	                        'userid': email,
	                        'first_name': first_name,
	                        'last_name': last_name,
	                        'password': password,
	                    })
             	return render(request,"upload.html")
    	 if(name2=='login'):
             email = request.POST.get('username','')
             password = request.POST.get('password','')
             print ("username is ", email, "password is ", password)
             email=str(email)
             password=str(password)
             s=''
             s=email+password
             response= encrypted_table.get_item(Key={
                        'userid': email
                    })
             if(len(response)==2): 
                item = response['Item']['password']
                if(password==item):
                    return render(request,"upload.html")
                else:
                    print("Invalid password")
                    return render(request,'index.html',{'s':["invalid password",'0']})
             else:
                print("Invalid Username")
                s1="invalid username"
                return render(request,'index.html',{'s':["invalid username",'0']})
             


def index(request):
	global input_folder,output_folder
	for the_file in os.listdir(input_folder):
	    file_path = os.path.join(input_folder, the_file)
	    try:
	        if os.path.isfile(file_path):
	            os.unlink(file_path)
	    except Exception as e:
	        print(e)
	for the_file in os.listdir(output_folder):
	    file_path = os.path.join(output_folder, the_file)
	    try:
	        if os.path.isfile(file_path):
	            os.unlink(file_path)
	    except Exception as e:
	        print(e)

	return render(request,"upload.html")

def upload(request):
	global file_name,input_folder
	myfile = request.FILES['file']
	file_name=myfile.name
	loc=input_folder+str(myfile.name)
	fs = FileSystemStorage(location='Spellcheck/UploadFiles/')
	filename = fs.save(myfile.name, myfile)
	sc.run(loc,str(myfile.name))

	return render(request,"download.html")


def download(request):
	global file_name,output_folder
	filename=file_name
	f = open(output_folder+filename, "r")
	response = HttpResponse(FileWrapper(f), content_type='application/txt')
	response['Content-Disposition'] = 'attachment; filename='+filename
	f.close()
	return response
