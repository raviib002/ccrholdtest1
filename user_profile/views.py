import requests
import json
import random
import string
from django.contrib.auth import views as auth_views
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.http import HttpResponseRedirect, HttpResponse
from django.urls.base import reverse_lazy
from django.conf import settings
from django.core.mail import (send_mail,
                              EmailMultiAlternatives,
                              EmailMessage
                              )
from django.utils.html import strip_tags, format_html
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext as _
from user_profile.forms import (LoginForm, 
                                PasswordResetFormUnique,
                                CustomPasswordChangeForm,
                                )
API_DOMAIN = settings.CASE_HISTORY_API['DOMAIN']
API_URL = settings.CASE_HISTORY_API['URL']



"""CCRH Functionality to check user existence in both apps - starts"""
def check_user_existance(request):
    """View for the login
    1) Checking user existance in CCRH & CASE HISTORY App
    3) Checks if user is valid and deactivated.
    """
    user_existance_in_app = ''
    message = case_action_url = password = None
    form = LoginForm(auto_id=False)
    if request.method == 'GET':
        return render(request, 'user_profile/login.html', {'form': form, })
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST, auto_id=False)
        if form.is_valid():
            username =request.POST['username']
            password =request.POST['password']
            ccrh_user=authenticate(username=username,password=password) #Checking user in CCRH App
            '''Case History User Check Start'''
            data = {'username':username,
                    'password':password
                }
            r = requests.post(url = API_DOMAIN+API_URL+'check_user/', data=data)
            try:
                result = r.json()
            except:
                result = {}
            case_history_user_status = result.get('status')
            '''Case History User Check End'''
            if ccrh_user and ccrh_user.is_active and case_history_user_status==1: #if user exist in CCRH & CASE HISTORY both APP
                user_existance_in_app = 'both'
            elif case_history_user_status: # User is only in CCRH CASE HISTORY APP
                if case_history_user_status == 1:
                    user_existance_in_app = 'case_history'
                else:
                    message = result.get('message')
            elif ccrh_user is not None: # User is only in CCRH Content APP
                if ccrh_user.is_active:
                    user_existance_in_app = 'ccrh'
                else:
                    message = _('Account is Blocked ! Please contact Admin')
            else:
                message = _('Login Failed! Please Verify Your Email and Password')
        else:
            message = _('Login Failed! Please Verify Your Email and Password')
        return render(request, 'user_profile/login.html', {'form':form,
                                                           "case_action_url" : settings.CASE_HISTORY_LOGIN_URL,
                                                           "password":password,
                                                           "user_existance_in_app":user_existance_in_app,
                                                            "message" : message,
                                                            })
"""CCRH Functionality to check user existence in both apps - ends"""

"""CCRH Login Functionality - starts"""
def login_view(request):
    form = LoginForm(auto_id=False)
    redirect_to = request.GET['next'] if request.GET else None
    if request.method == 'GET':
        if request.user.is_authenticated and not request.user.is_superuser:
            return HttpResponseRedirect('/dashboard/')
        elif request.user.is_authenticated and request.user.is_superuser:
            return HttpResponseRedirect('/admin/')
        else:
            return render(request, 'user_profile/login.html', { 'form': form, })
            
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST, auto_id=False)
        if form.is_valid():
            username =request.POST['username']
            password =request.POST['password']
            user=authenticate(username=username,password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if user.is_superuser:
                        return HttpResponseRedirect('/admin/')
                    if redirect_to:
                        return HttpResponseRedirect(redirect_to)
                    else:
                        return HttpResponseRedirect(reverse_lazy('user_profile:dashboard'))
                else:
                    message = _('Account is Blocked ! Please contact Admin')
            else:
                message = _('Login Failed! Please Verify Your Email and Password')
        else:
            message = _('Login Failed! Please Verify Your Email and Password')
        return render(request, 'user_profile/login.html', {'form':form,
                                                            "message" : message,
                                                            })
"""CCRH Login Functionality - ends"""
     
"""CCRH Logout Functionality - starts"""     
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
"""CCRH Logout Functionality - ends"""
   
   
"""Forgot Password functionality. - Starts"""
def password_forgot(request):
    fp_form = PasswordResetFormUnique()
    success = request.session.pop('success', None)
    #To show invalid email error message - starts
    old_post = request.session.pop('_old_post', None)
    if old_post:
        fp_form = PasswordResetFormUnique(old_post)
    
    if request.method == 'GET':
        form = PasswordResetFormUnique()
        return render(request, 'user_profile/forget_password.html',{'form':form,
                                                                    'fpform':fp_form,
                                                                    'old_post':old_post,
                                                                    'success':success,
                                                                    })
    
    elif request.method == 'POST':
        form = PasswordResetFormUnique(request.POST)
        if form.is_valid():
            request.session['success'] = _('We have sent a link to change your password. Kindly check your email.')
            return auth_views.PasswordResetView.as_view(
                            form_class = PasswordResetFormUnique,
                            template_name = 'user_profile/forget_password.html',
                            email_template_name = 'user_profile/password_reset_email.html',
                            success_url = reverse_lazy('user_profile:forget_password'),
                            )(request)
        else:
            request.session['_old_post'] = request.POST
            return HttpResponseRedirect(reverse_lazy('user_profile:forget_password'))
            return render (request, 'user_profile/forget_password.html',{'form':form,
                                                                         'fpform':fp_form,
                                                                         })
    else:
        return HttpResponseRedirect(reverse_lazy('user_profile:forget_password'))
"""Forgot Password functionality. - Ends"""


"""Change Password functionality. - Starts"""
@login_required  
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return render(request, 'user_profile/password_change.html', {'form': form,
                                                                      'note':'success'})
        else:
            return render(request, 'user_profile/password_change.html', {'form': form })
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'user_profile/password_change.html', {'form': form })

"""Change Password functionality. - Ends"""
