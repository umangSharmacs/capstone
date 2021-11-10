from django.urls import path
from .views import homepage, sensordata, updatechart, signupView, login_view, logout_view, sensor1, sensor2, sensor3, sensor4, user_info, placeholder

urlpatterns=[
    path('sensordata/', sensordata, name='sensordata'),
    path('sensor1/', sensor1, name='sensor1'),
    path('sensor2/', sensor2, name='sensor2'),
    path('sensor3/', sensor3, name='sensor3'),
    path('sensor4/', sensor4, name='sensor4'),
    path('', homepage.as_view(), name='home'),
    path('updatechart/', updatechart, name='updatechart'),
    path('user_info/', user_info, name='user_info'),
    path('404/', placeholder, name='404'),
    path('signup/', signupView.as_view(), name='signup'),
    path('login/', login_view.as_view(), name='login'),
    path('logout/', logout_view, name='logout')
]