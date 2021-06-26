
from django.shortcuts import render, redirect
from .models import *
from django.core.exceptions import PermissionDenied


def index(request):
    return render(request,'login.html')

# --------------------------------> LOGIN and REGISTER VIEWS <--------------------------------
def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    elif request.method =='POST':
        errors = User.objects.login_validations(request.POST)
        if len(errors)>0:
            context = {
                'errors':errors
            }
            return render(request, 'login.html', context)
        else:
            user = User.objects.filter(email=request.POST['email'])[0]
            request.session['id'] = user.id
            return redirect('/success')
        
        
def register(request):
    if request.method=='GET':
        return render(request, 'register.html')
    elif request.method =='POST':
        errors = User.objects.basic_validations(request.POST)
        if len(errors)>0:
            context = {
                'errors':errors
            }
            return render(request, 'register.html', context)
        else:
            hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()      
            user=User.objects.first()
            newuser=User.objects.create(
                first_name=request.POST['first_name'],
                last_name= request.POST['last_name'],
                email= request.POST['email'],
                password= hash1)                
            newuser.save()
            request.session['id'] = newuser.id
        return redirect('/success')


def success(request):
    if 'id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['id'])
    context = {
        'user' : user
    }
    return render(request, 'success.html', context)


def logout(request):
    request.session.clear()
    return redirect('/login')