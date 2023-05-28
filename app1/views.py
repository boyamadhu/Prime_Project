from django.shortcuts import render
from app1.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.

def register(request):
    ufo=UserForm()
    pfo=ProfileForm()
    d={'ufo':ufo,'pfo':pfo}

    if request.method=='POST' and request.FILES:
        ufd=UserForm(request.POST)
        pfd=ProfileForm(request.POST,request.FILES)
        if ufd.is_valid() and pfd.is_valid():
            NSUO=ufd.save(commit=False)
            password=ufd.cleaned_data['password']
            NSUO.set_password(password)
            NSUO.save()

            NSPO=pfd.save(commit=False)
            NSPO.username=NSUO
            NSPO.save()
            send_mail('Registering prime','Congrats You have successfully registered amazon prime', 
                      'boyamadhus9493@gmail.com',[NSUO.email],fail_silently=False)
            return HttpResponseRedirect(reverse('prime'))
        else:
            return HttpResponse('Not valid')

    return render(request,'register.html',d)

def user_login(request):
    if request.method=='POST':
        un=request.POST['email']
        pw=request.POST['password']
        AO=authenticate(username=un,password=pw)
        if AO and AO.is_active:
            login(request,AO)
            request.session['username']=un
            
            return HttpResponseRedirect(reverse('prime_home'))
        else:
            return render(request,'first.html')

    return render(request,'first.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('prime'))

@login_required
def display_profile(request):
    username=request.session.get('username')
    UO=User.objects.get(username=username)
    PO=Profile.objects.get(username=UO)
    d={'UO':UO,'PO':PO}
    return render(request,'dummy.html',d)

def prime(request):
    return render(request,'prime.html')

def dummy(request):
    return render(request,'dummy.html')

def prime_home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        UO=User.objects.get(username=username)
        PO=Profile.objects.get(username=UO)
        d={'UO':UO, 'PO':PO, 'username':username}
        return render(request,'prime_home.html',d)
    return render(request,'prime_home.html')

def catagories(request):
    if request.session.get('username'):
        username=request.session.get('username')
        UO=User.objects.get(username=username)
        PO=Profile.objects.get(username=UO)
        d={'UO':UO, 'PO':PO, 'username':username}
        return render(request,'catagories.html',d)
    
    return render(request,'catagories.html')

def create_account(request):
    return render(request,'create_account.html')

def store(request):
    if request.session.get('username'):
        username=request.session.get('username')
        UO=User.objects.get(username=username)
        PO=Profile.objects.get(username=UO)
        d={'UO':UO, 'PO':PO, 'username':username}
        return render(request,'store.html',d)
    return render(request,'store.html')

def practice(request):
    return render(request,'practice.html')

@login_required
def update_password(request):
    if request.method=='POST':
        OP=request.POST['oldpass']
        NO=request.POST['newpass']
        if NO:
            if OP==NO:
                username=request.session.get('username')
                OB=User.objects.get(username=username)
                OB.set_password(NO)
                OB.save()
                logout(request)
                return HttpResponseRedirect(reverse('prime'))
            else:
                return HttpResponse('password is not matched')
        else:
            return HttpResponse('please type password')
    return render(request,'update_password.html')


def forgot_password(request):
    if request.method=='POST':
        un=request.POST['username']
        pw=request.POST['newpass']
        rw=request.POST['repass']
        UO=User.objects.filter(username=un)
        if UO:
            if pw==rw:
                UO=User.objects.get(username=un)
                UO.set_password(pw)
                UO.save()
                return render(request,'prime.html')
            else:
                return HttpResponse('Password is not Matched')
        else:
            return HttpResponse('User is not available')
    return render(request,'forgot_password.html')