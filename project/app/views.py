from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Student
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def index(request):
    data=Student.objects.all()
    print(data)
    context={"data":data}
    return render(request, "index.html", context)

def insertData(request):
    data=Student.objects.all()
    context={'data':data}
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        age=request.POST['age']
        gender=request.POST['gender']
        print(name, email, age, gender)
        query=Student(name=name, email=email, age=age, gender=gender)
        query.save()
        messages.info(request, "Data Inserted Successfully")
        return redirect("/")
    return render(request, "index.html", context)

def updateData(request, id):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        age=request.POST.get('age')
        gender=request.POST.get('gender')

        edit=Student.objects.get(id=id)
        edit.name=name
        edit.email=email
        edit.gender=gender
        edit.age=age
        edit.save()
        messages.warning(request, "Data Updated Successfully")
        return redirect("/")
        
    d=Student.objects.get(id=id)
    context={"d":d}
    return render(request, "edit.html", context)

def deleteData(request, id):
    d=Student.objects.get(id=id)
    d.delete()
    messages.error(request, "Data Deleted Successfully")
    return redirect("/")

def about(request):
    return render(request, "about.html")

def signup(request):
    if request.method == "POST":
        uname=request.POST.get('name')
        email=request.POST.get('email')
        pass1=request.POST.get('psw')
        pass2=request.POST.get('psw-repeat')

        if pass1 != pass2:
            messages.error(request, "Your Password and Repeat Password are not matching")
            return redirect('signup')
        else:
            my_user=User.objects.create_user(uname, email, pass1)
            my_user.save()
            return redirect("login")

    return render(request, "signup.html")

def loginpage(request):
    if request.method=="POST":
        username=request.POST.get('name')
        password=request.POST.get('psw')
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "You have entered incorrect details.")
            return redirect('login')

    return render(request, "login.html")

def logoutpage(request):
    logout(request)
    return redirect('login')