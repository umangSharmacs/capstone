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
# # Create your views here.

# INTEGRATING FIREBASE WITH DJANGO------------------------------------------------- 

config={ 
  "apiKey": "AIzaSyC9efTd_7mPW1tI0FGNWdC1NXHqyz9qIyE",
  "authDomain": "test-381c5.firebaseapp.com",
  "databaseURL": "https://test-381c5-default-rtdb.firebaseio.com",
  "projectId": "test-381c5",
  "storageBucket": "test-381c5.appspot.com",
  "messagingSenderId": "38012413586",
  "appId": "1:38012413586:web:e6350fc379929955dc684b",
  "measurementId": "G-DDF1PXLKKL",
  "serviceAccount": "C:\\Users\\umang\\Desktop\\CapStone\\website\\dashboard\\app\\test-381c5-firebase-adminsdk-y6i8d-48ded77d9f.json"
}

firebase=pyrebase.initialize_app(config)
authe = firebase.auth()

database=firebase.database()

def preprocess(data: str) -> list:
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

def sensordata(request):
  numbers=[]
  a=database.child(f'{request.user.username}').get()
  try:
    for i in a.each():
      
      if i.val():
        numbers.append(preprocess(i.val()))
    numbers=sum(numbers,[])
    
    return render(request,'sensordata.html' ,{"data":numbers})
  except:
    return render(request,'sensordata.html' ,{"data":0})

def updatechart(request):
  firebase=pyrebase.initialize_app(config)
  authe = firebase.auth()

  database=firebase.database()
  database.child('umang123').push(str(round(random.uniform(3.4,140.0), 3)))
  if request.is_ajax and request.method == "GET":
    firebase=pyrebase.initialize_app(config)
    authe = firebase.auth()
    database=firebase.database()
    
    numbers=[]
    a=database.child(f'{request.user.username}').get()
    if a.each() is not None:
      for i in a.each():
        if i.val():
          numbers.append(preprocess(i.val()))
      numbers=sum(numbers,[])
      return JsonResponse({"data": numbers})
    return JsonResponse({'data': 0})

def test(request):
  times=[]
  a=database.child(f'time').get()
  for i in a.each():
    time = datetime.datetime.fromtimestamp(i.val()/1000)
    times.append(time)
  return render(request,'test.html', {'times': times})

class overview(TemplateView):
  template_name='overview.html'

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

  