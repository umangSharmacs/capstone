from django.urls import path
from .views import homepage, overview, sensordata, updatechart, signupView, test, login_view, logout_view

urlpatterns=[
    path('overview/', overview.as_view(), name='overview'),
    path('sensordata/', sensordata, name='sensordata'),
    path('', homepage.as_view(), name='home'),
    path('updatechart/', updatechart, name='updatechart'),
    path('signup/', signupView.as_view(), name='signup'),
    path('test/', test, name='test'),
    path('login/', login_view.as_view(), name='login'),
    path('logout/', logout_view, name='logout')
]