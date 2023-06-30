from django.urls import path, include
from . import views
from smsgateaway import views as smsviews
urlpatterns = [
    path('', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('enter/', smsviews.sms_gateway_view, name='enter')
]
