from django.shortcuts import render, HttpResponse, redirect
from .models import Users
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, "index.html")

def success(request):
    if not 'user_id' in request.session:
        messages.error(request, "Please log in", extra_tags="invalid_access")
        return redirect("/")
    
    user = Users.objects.get(id=request.session['user_id'])
    context={
        "first_name": user.first_name,
    }
    return render(request, "success.html", context)

def register(request):
    errors = Users.objects.validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect("/")
    else:
        request.session['user_id'] = Users.objects.register(request.POST)
        return redirect("/success")

def login(request):
    errors = Users.objects.login(request.POST)
    if errors != None:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
            print(messages)
        return redirect("/")
    else:
        request.session['user_id'] = Users.objects.get(email=request.POST['email']).id
        return redirect("/success")

def logout(request):
    keys = []
    for key in request.session.keys():
        keys.append(key)
    for key in keys:
        del request.session[key]
    return redirect("/")