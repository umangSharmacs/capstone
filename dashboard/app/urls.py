from django.urls import path, include
from .views import change_password, homepage, sensordata, updatechart, signupView, login_view, logout_view, sensor1, sensor2, sensor3, sensor4, user_info, placeholder, change_password, system_messages,password_reset, sharedata
from django.contrib.auth import views as auth_views

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
    path('logout/', logout_view, name='logout'),
    path('changepassword/', change_password, name='changepassword'),
    path('system_messages/', system_messages, name='system_messages'),
    #path('accounts/', include('django.contrib.auth.urls')),
    path("password_reset/", password_reset, name="tpassword_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'),
    path('sharedata/', sharedata, name="sharedata"),     
]