from django.shortcuts import render
from .forms import UserForm, UserProfileInfoForm

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request,"index_page.html")

@login_required # To view this function the user should login. Otherwise can't.
def special(request):
    return render(request, 'index_page.html')

@login_required # To view this function the user should login. Otherwise can't.
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('thanks'))


def register(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
                # profile_pic is the name taken from UserProfileInfo model.
                # As profile pic is a file, so we find it in request.FILES

            profile.save()
            registered = True

            return HttpResponseRedirect(reverse('accounts:login'))
        else:
            print(user_form.errors,profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'accounts/registration.html',
                    {'user_form':user_form,
                    'profile_form':profile_form,
                    'registered':registered})


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password = password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('test'))
            else:
                return HttpResponse("Your Account is not Active. Please Login!")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")
    else:
        now_registered = True
        return render(request, 'accounts/login.html',{'now_registered':now_registered})
