from django.urls import path
from . import views

app_name = 'smsgateaway' 
urlpatterns = [
    path('input/', views.sms_gateway_view, name='input'),  
    path('result/', views.result_view, name='result'),
]
