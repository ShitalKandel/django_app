from django.shortcuts import render,redirect
from .models import signupform,singinform
from django.contrib.auth import login



def signupView(request):
    if request.method == "POST":
        form = signupform(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('login.html') 
    else:
        form = signupform()
    return render(request, 'register.html', {'form': form})

def loginView(request):
    if request.method == "POST":
        form = singinform(request.POST)
        if form.is_valid() == signupform:
            login(login)

    return render(request, 'login.html') 

