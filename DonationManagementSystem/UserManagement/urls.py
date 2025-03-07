from django.urls import path
from .views import Login,Register,Profile,log_out,ErrorView

app_name = 'UserManagement'
urlpatterns=[
    path('',Profile.as_view(),name='profile'),
    path('login/',Login.as_view(),name='login'),
    path('register/',Register.as_view(),name='register'),
    path('logout/',log_out, name='logout'),
    path('error/',ErrorView.as_view(), name='error'),
]
