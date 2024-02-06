from django.shortcuts import render,redirect
from .models import signupform


def signupView(request):
    if request.method == "POST":
        form = signupform(request.POST)
        if form.is_valid():
            form.save()
            return redirect(request, 'login.html') 
        # form = signupform()  
    else:
        return render(request, 'register.html', {'form': form})

def loginView(request):
    if request.method == "POST":
        pass
    return render(request, 'login.html') 