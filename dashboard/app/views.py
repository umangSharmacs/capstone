# username: surynash
# password: umangprakharsuryansh

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

def preprocess_old(data: str) -> list:
  '''
  OLD FUNCTION FOR PREVIOUS FIREBASE. WHEN DATA WAS BEING UPLOADED BY ARDUINO AND THERE WERE NO SPACES ETC.
  '''
  processed_list=[]
  digits=[]
  for index,i in enumerate(data):
    if i=='\r' or i=='\n':
      if digits!=[]:
        processed_list.append(float(''.join(digits)))
        digits=[]
        continue
    else:
      digits.append(i)
  if digits!=[]:
    processed_list.append(float(''.join(digits)))
  return processed_list

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
  # numbers=[]
  # a=database.child(f'{request.user.username}').get()
  # try:
  #   for i in a.each():
      
  #     if i.val():
  #       numbers.append(preprocess(i.val()))
  #   numbers=sum(numbers,[])
    
  #   return render(request,'sensordata.html' ,{"data":numbers})
  # except:
  #   return render(request,'sensordata.html' ,{"data":0})

  '''
  CODE ABOVE IS ALSO OLD CODE. USED FOR WHEN ARDUINO WAS USED.

  CODE BELOW IS USED FOR THE ARTIFICIAL CODE.
  '''
  sensor1,sensor2,sensor3,sensor4,_,time=get_data(request)
  return render(request,'sensordata.html', {"sensor1": sensor1, "sensor2": sensor2, "sensor3": sensor3, "sensor4": sensor4, "time":time})

def get_indices(zipped_list):
  '''
  GEt errors where sensors weren't able to send data. Implemented in artificial data using negative numbers.
  '''
  to_notify=[]
  for i in zipped_list:
    if i[0]<=0:
      to_notify.append(1)
    else:
      to_notify.append(0)
  return to_notify

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
  sensor1,sensor2,sensor3,sensor4,time, time_json=get_data(request)
  sensor1_errors=get_indices(zip(sensor1, time))
  sensor2_errors=get_indices(zip(sensor2, time))
  sensor3_errors=get_indices(zip(sensor3, time))
  sensor4_errors=get_indices(zip(sensor4, time))
  result=check(sensor1, sensor2, sensor3, sensor4, time)
  data={
    "sensor1": sensor1,
    "sensor2": sensor2,
    "sensor3": sensor3,
    "sensor4": sensor4,
    "time": time_json,
    "sensor1_errors": sensor1_errors,
    "sensor2_errors": sensor2_errors,
    "sensor3_errors": sensor3_errors,
    "sensor4_errors": sensor4_errors,
    "result": result}
  return JsonResponse(data, safe=False)

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
    res.append((sensor1[i]+sensor2[i]+sensor3[i]+sensor4[i])/c)
  res=[1 if i>40 else 0 for i in res]  
  return res

''' 
BELOW FUNCTIONS ARE FOR THE INDIVIDUAL SENSOR PAGES.
'''

def sensor1(request):
  sensor1_data,sensor2_data,sensor3_data,sensor4_data,time, time_json=get_data(request)
  to_notify=get_indices(zip(sensor1_data, time))
  res=check(sensor1_data, sensor2_data, sensor3_data, sensor4_data, time)
  return render(request,'sensor1.html', {"sensor1": sensor1_data, "time":time_json, "to_notify": to_notify, "result": res})

def sensor2(request):
  sensor1_data,sensor2_data,sensor3_data,sensor4_data,time, time_json=get_data(request)
  to_notify=get_indices(zip(sensor2_data, time))
  res=check(sensor1_data, sensor2_data, sensor3_data, sensor4_data, time)
  return render(request,'sensor2.html', {"sensor2": sensor2_data, "time":time_json, "to_notify": to_notify, "result": res})

def sensor3(request):
  sensor1_data,sensor2_data,sensor3_data,sensor4_data,time, time_json=get_data(request)
  to_notify=get_indices(zip(sensor3_data, time))
  res=check(sensor1_data, sensor2_data, sensor3_data, sensor4_data, time)
  return render(request,'sensor3.html', {"sensor3": sensor3_data, "time":time_json, "to_notify": to_notify, "result": res})

def sensor4(request):
  sensor1_data,sensor2_data,sensor3_data,sensor4_data,time, time_json=get_data(request)
  to_notify=get_indices(zip(sensor4_data, time))
  res=check(sensor1_data, sensor2_data, sensor3_data, sensor4_data, time)
  return render(request,'sensor4.html', {"sensor4": sensor4_data, "time":time_json, "to_notify": to_notify, "result": res})

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
  return render(request,'user_info.html', {"username": request.user.username })