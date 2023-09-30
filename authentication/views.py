from django.shortcuts import render,redirect
#importo la clase UserCreationForm
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login,logout,authenticate #este login va acrear un cookie por nosotros
from django.db import IntegrityError

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                #registrar usuario
                user=User.objects.create_user(username=request.POST['username'],password=request.POST['password1'])
                #se guarda dentro de la base de datos
                user.save()
                return redirect('signin')          
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error':"Usuario ya existe"
                })         
        #cuando no coinciden las contraseñas
        return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error':"Contraseñas no coinciden"
        })
#cerrar sesion
def signout(request):
    logout(request)
    return redirect('signin')
def home(request):
    return render(request,'home.html')
#inicio sesion    
def signin(request):
   if request.method == 'GET':
        return render(request,'login.html',{
        'form':AuthenticationForm
    })
   else:
       user=authenticate(request, username=request.POST['username'], password=request.POST['password'])
       if user is None:
           return render(request,'login.html',{
          'form':AuthenticationForm,
          'error':"Usuario o contraseña incorrecta"
        })
       else:
           login(request, user)
           return redirect('home')