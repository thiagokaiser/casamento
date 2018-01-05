from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import (
    authenticate,
    login,
    update_session_auth_hash
    )
from django.contrib.auth.forms import (
    UserChangeForm, 
    UserCreationForm, 
    PasswordChangeForm
    )
from .forms import (    
    EditProfileForm,
    RegisterProfileForm,    
    )


# Create your views here.
def Home(request):
	return render(request, 'app/base.html', {})

def Profile(request):
    args = {'user': request.user}
    return render(request, 'accounts/profile.html', args)

def Edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('app:profile')

    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'accounts/edit_profile.html', args)

def Register(request):
    if request.method == 'POST':
        form = RegisterProfileForm(request.POST)
        if form.is_valid():
            form.save()
            
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('app:profile')            
                
        args = {'form': form}
        return render(request,'accounts/register.html', args)
        
    else:
        form = RegisterProfileForm()
        args = {'form': form}
        return render(request,'accounts/register.html', args)

def Change_Password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('app:profile')
        else:
            args = {'form': form}
            return render(request,'accounts/change_password.html', args)


    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'accounts/change_password.html', args)
