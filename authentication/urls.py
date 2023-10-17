from django.urls import path
from . import views

urlpatterns = [
     path('',views.signin,name="signin"),
    path('Anahion/signup',views.signup,name="signup"),
    path('Anahion/home/',views.home,name="home"),
    path('Anahion/logout/',views.signout,name="signout")
   
]
