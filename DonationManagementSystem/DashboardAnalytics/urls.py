from django.urls import path
from . import views

app_name = 'DashboardAnalytics'
urlpatterns =[
    path('',views.dashboard,name='dashboard'),
    path('donated',views.my_donations,name='donated'),
    path('requests',views.my_requests,name='requests'),
]
