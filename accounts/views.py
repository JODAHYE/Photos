from django.shortcuts import render

# Create your views here.
from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


# Create your views here.
def signup(request):
    if request.user.is_anonymous:
        if request.method == "POST":
            if request.POST["password"] == request.POST["passwordCheck"]:
                if request.POST["username"] != '':
                    if User.objects.filter(username=request.POST["username"]).exists():
                        return render(request, 'accounts/signupError.html')
                    user = User.objects.create_user(
                        username=request.POST["username"], email=request.POST["email"], password=request.POST["password"]
                    )
                    auth.login(request, user)
                    return redirect('/')
                else:
                    return render(request, 'accounts/signup.html')
            else:
                return render(request, 'accounts/passwordCheckError.html')
        return render(request, 'accounts/signup.html')
    return redirect('/')


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            return render(request, 'accounts/login.html', {'error': 'Please enter your correct email and password'})
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')