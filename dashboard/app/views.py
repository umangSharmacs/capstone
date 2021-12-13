# username: suryansh
# password: umangprakharsuryansh

from logging import error
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView   
from django.urls import reverse_lazy
from django.views import generic
import random
import pyrebase
from django.views.generic import TemplateView
from .forms import CustomUserForm
from .forms import LoginForm
import datetime
import json

from django.conf import settings
from django.core.mail import send_mail

# # Create your views here.

# INTEGRATING FIREBASE WITH DJANGO------------------------------------------------- 

# NOTE: BELOW CONFIG IS FOR THE FIREBASE DATABASE IN WHICH ACTUAL SENSOR DATA WILL BE PUT.
# config={ 
#   "apiKey": "AIzaSyC9efTd_7mPW1tI0FGNWdC1NXHqyz9qIyE",
#   "authDomain": "test-381c5.firebaseapp.com",
#   "databaseURL": "https://test-381c5-default-rtdb.firebaseio.com",
#   "projectId": "test-381c5",
#   "storageBucket": "test-381c5.appspot.com",
#   "messagingSenderId": "38012413586",
#   "appId": "1:38012413586:web:e6350fc379929955dc684b",
#   "measurementId": "G-DDF1PXLKKL",
#   "serviceAccount": "C:\\Users\\umang\\Desktop\\CapStone\\website\\dashboard\\app\\test-381c5-firebase-adminsdk-y6i8d-48ded77d9f.json"
# }

# firebase=pyrebase.initialize_app(config)

#NOTE: BELOW CONFIG IS FOR TESTING. PYTHON SCRIPT WITH RANDOM INPUTS IS ENTERED INTO IT.
# CHANGE THE 'SERVICEACCOUNT' PATH WHEN YOU RUN THE CODE
config ={
  "apiKey": "AIzaSyASlcy_j8dDzq8640Pu8q1UfxfsLqSM2ZQ",
  "authDomain": "capstone-7efdb.firebaseapp.com",
  "databaseURL": "https://capstone-7efdb-default-rtdb.firebaseio.com",
  "projectId": "capstone-7efdb",
  "storageBucket": "capstone-7efdb.appspot.com",
  "messagingSenderId": "680684474246",
  "appId": "1:680684474246:web:8aa5aff0dfa0fdfe7da607",
  "serviceAccount":"C:\\Users\\umang\\Desktop\\CapStone\\website\\dashboard\\app\\capstone-7efdb-firebase-adminsdk-vxpkn-ab0dde8e90.json"
}

firebase=pyrebase.initialize_app(config)

authe = firebase.auth()

database=firebase.database()

def get_data(request):
  '''
  HELPER FUNCTION TO GET ALL THE DATA FROM FIREBASE
  '''
  sensor1=[]
  sensor2=[]
  sensor3=[]
  sensor4=[]
  time=[]
  a=database.child(f'{request.user.username}').get()
  try:
    for i in a.each():
      sensor1.append(i.val()['sensor1'])
      sensor2.append(i.val()['sensor2'])
      sensor3.append(i.val()['sensor3'])
      sensor4.append(i.val()['sensor4'])
      time.append(i.val()['time'])
  except:
    sensor1.append(0)
    sensor2.append(0)
    sensor3.append(0)
    sensor4.append(0)
    time.append(0)
  time_json=json.dumps(time)
  return sensor1,sensor2,sensor3,sensor4,time, time_json

def sensordata(request):
  sensor1,sensor2,sensor3,sensor4,_,time,_=get_errors(request)
  current_sensor1=round(sensor1[-1],2)
  current_sensor2=round(sensor2[-1], 2)
  current_sensor3=round(sensor3[-1],2)
  current_sensor4=round(sensor4[-1],2)
  return render(request,'sensordata.html', {"sensor1": sensor1, "sensor2": sensor2, "sensor3": sensor3, "sensor4": sensor4, "time":time, "current_sensor1": current_sensor1, "current_sensor2": current_sensor2, "current_sensor3": current_sensor3, "current_sensor4": current_sensor4})

def get_errors(request):
  sensor1,sensor2,sensor3,sensor4,time,time_json=get_data(request)
  
  errors_list=[]
  for index,_ in enumerate(sensor1):
    t1=[]
    t1.append(str(time[index]))
    t=[]
    if sensor1[index]=="error":
      t.append("Temperature")
    if sensor2[index]=="error":
      t.append("pH")
    if sensor3[index]=="error":
      t.append("Turbidity")
    if sensor4[index]=="error":
      t.append("TDS")
    if len(t)==0:
      t.append("No Errors")
    t1.append(t)
    errors_list.append(t1)
  s=zip(sensor1, sensor2, sensor3, sensor4, time)
  s= list(filter(lambda c: c[0]!="error" and c[1]!="error" and c[2]!="error" and c[3]!="error", s))
  sensor1_data=[i[0] for i in s]
  sensor2_data=[i[1] for i in s]
  sensor3_data=[i[2] for i in s]
  sensor4_data=[i[3] for i in s]
  time=[i[4] for i in s]
  time_json=json.dumps(time)
  return sensor1_data, sensor2_data, sensor3_data, sensor4_data, time, time_json, errors_list


def system_messages(request):
  '''
  Get errors where sensors weren't able to send data. Implemented in data using "error".
  '''
  _,_,_,_,_,_,errors_list=get_errors(request)
  if errors_list!=[]:
    alert_user(request)
  
  return render(request,'system_messages.html', {"errors_list": errors_list})

from copy import deepcopy
def outlier_detection(zipped_list):
  og=deepcopy(zipped_list)
  l=sorted(zipped_list)
  q1=l[int((len(l)+1)//4)]
  q3=l[int(3*(len(l)+1)//4)]
  iqr=q3[0]-q1[0]
  lb=q1[0]-1.5*iqr
  ub=q3[0]+1.5*iqr
  r=[]
  for i in og:
    if lb<=i[0]<=ub:
      r.append(0)
    else:
      r.append(1)
  return r

def updatechart(request):
  '''
  Function to update data for ajax calls. 
  UPdates a webpage at '/updatechart/' from which the ajax can get updated data.
  '''

  firebase=pyrebase.initialize_app(config)
  authe = firebase.auth()

  database=firebase.database()
  
  firebase=pyrebase.initialize_app(config)
  authe = firebase.auth()
  database=firebase.database()
  sensor1, sensor2, sensor3, sensor4, time, time_json, errors_list=get_errors(request)
  sensor1_errors=outlier_detection(zip(sensor1, time))
  sensor2_errors=outlier_detection(zip(sensor2, time))
  sensor3_errors=outlier_detection(zip(sensor3, time))
  sensor4_errors=outlier_detection(zip(sensor4, time))
  result=check(sensor1, sensor2, sensor3, sensor4, time)
  data={
    "sensor1": sensor1,
    "sensor2": sensor2,
    "sensor3": sensor3,
    "sensor4": sensor4,
    "current_sensor1": round(sensor1[-1],2),
    "current_sensor2": round(sensor2[-1],2),
    "current_sensor3": round(sensor3[-1],2),
    "current_sensor4": round(sensor4[-1],2),
    "time": time_json,
    "sensor1_errors": sensor1_errors,
    "sensor2_errors": sensor2_errors,
    "sensor3_errors": sensor3_errors,
    "sensor4_errors": sensor4_errors,
    "result": result}
  print(type(time_json))
  return JsonResponse(data, safe=True)

def check(sensor1, sensor2, sensor3, sensor4, time):
  '''
  CODE TO CLASSIFY WATER. 
  CURRENTLY IF AVERAGE>40 THEN WATER IS SUITABLE.
  '''
  res=[]
  for i in range(len(time)):
    c=0
    if sensor1[i]!=0:
      c+=1
    if sensor2[i]!=0:
      c+=1
    if sensor3[i]!=0:
      c+=1
    if sensor4[i]!=0:
      c+=1
    if c==0:
      res.append(0)
    else:
      res.append((sensor1[i]+sensor2[i]+sensor3[i]+sensor4[i])/c)
  res=[1 if i>40 else 0 for i in res]
  return res

''' 
BELOW FUNCTIONS ARE FOR THE INDIVIDUAL SENSOR PAGES.
'''

def sensor1(request):
  sensor1_data,sensor2_data,sensor3_data,sensor4_data,time,time_json,_=get_errors(request)
  to_notify=outlier_detection(zip(sensor1_data, time))
  res=check(sensor1_data, sensor2_data, sensor3_data, sensor4_data, time)
  for i in res:
    if i==0:
      alert_user(request)
  return render(request,'sensor1.html', {"sensor1": sensor1_data, "time":time_json, "to_notify": to_notify, "result": res})
  

def sensor2(request):
  sensor1_data,sensor2_data,sensor3_data,sensor4_data,time,time_json,_=get_errors(request)
  to_notify=outlier_detection(zip(sensor2_data, time))
  res=check(sensor1_data, sensor2_data, sensor3_data, sensor4_data, time)
  for i in res:
    if i==0:
      alert_user(request)
  return render(request,'sensor2.html', {"sensor2": sensor2_data, "time":time_json, "to_notify": to_notify, "result": res})

def sensor3(request):
  sensor1_data,sensor2_data,sensor3_data,sensor4_data,time,time_json,_=get_errors(request)
  to_notify=outlier_detection(zip(sensor3_data, time))
  res=check(sensor1_data, sensor2_data, sensor3_data, sensor4_data, time)
  for i in res:
    if i==0:
      alert_user(request)
  return render(request,'sensor3.html', {"sensor3": sensor3_data, "time":time_json, "to_notify": to_notify, "result": res})

def sensor4(request):
  sensor1_data,sensor2_data,sensor3_data,sensor4_data,time,time_json,_=get_errors(request)
  to_notify=outlier_detection(zip(sensor4_data, time))
  res=check(sensor1_data, sensor2_data, sensor3_data, sensor4_data, time)
  for i in res:
    if i==0:
      alert_user(request)
  return render(request,'sensor4.html', {"sensor4": sensor4_data, "time":time_json, "to_notify": to_notify, "result": res})

def alert_user(request):
  subject = 'An Outlier has been detected'
  message = f'Hi {request.user.username}. During the regular check ups, an outlier data point was detected. Please check your dashboard for further info.'
  email_from = settings.EMAIL_HOST_USER
  send_mail( subject, message, email_from, [request.user.email])

def placeholder(request):
  return render(request, '404.html')

class homepage(TemplateView):
  template_name='homepage.html'

class signupView(generic.CreateView):
    form_class = CustomUserForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class login_view(LoginView):
  template_name = 'registration/login.html'
  form_class = LoginForm



from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('home')


def user_info(request):
  return render(request,'user_info.html', {"username": request.user.username,"email":request.user.email})

def sharedata(request):
  subject = f'Data shared by {request.user.username}'
  message = get_data(request)
  email_from = request.user.email
  try:
    send_mail( subject, message, email_from, [settings.EMAIL_HOST_USER])
  except:
    print("Error in emailing")
  return render(request, 'sharedata.html')

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'changepassword.html', {
        'form': form
    })



from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
def password_reset(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "main/password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})