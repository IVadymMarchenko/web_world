from django.shortcuts import render,HttpResponse

# Create your views here.



def home(request):
    return render(request,'app_home/index.html',context={'msg':'Hello World dddd'}) 


def profile(request):
    return render(request,'app_home/profile.html',context={'msg':'Your Profile'}) 


def registration(request):
    return render(request,'app_home/register_form.html',context={'msg':'Registration'}) 


def edit_profile(request):
    return render(request,'app_home/edit_profile.html',context={'msg':'Edit Profile'})