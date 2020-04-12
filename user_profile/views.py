import json
import random
import string
from django.contrib.auth import views as auth_views
from django.db import connection
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from user_profile.forms import LoginForm, PasswordResetFormUnique
from django.http import HttpResponseRedirect, HttpResponse
from django.urls.base import reverse_lazy
from django.conf import settings
from user_profile.forms import ( CustomPasswordChangeForm,RegistrationStep3)
from django.contrib.auth import views as auth_views
from django.core.mail import (send_mail,
                              EmailMultiAlternatives,
                              EmailMessage
                              )
from django.utils.html import strip_tags, format_html
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
# from user_profile.models import UserProfile
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.utils.translation import ugettext as _
from utils.common_functions import (make_unique_username)

from user_profile.models import AdditionalProfile
from master.models import State,City



"""CCRH Login Functionality - starts"""
def login_view(request):
    """View for the login
    1) Already login in are not
    2) Direct navigation logic after success login
    3) Checks if user is valid and deactivated.
    """
    form = LoginForm(auto_id=False)
    redirect_to = request.GET['next'] if request.GET else None
    
    if request.method == 'GET':
        if request.user.is_authenticated and not request.user.is_superuser:
            return HttpResponseRedirect('/dashboard/')
        elif request.user.is_authenticated and request.user.is_superuser:
            return HttpResponseRedirect('/admin/')
        else:
            return render(request,
                          'user_profile/login.html', {'form': form,
                                                     })
            
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
                message = _('Login Failed! Please Verify Your Email or Mobile No. and Password')
        else:
            message = _('Login Failed! Please Verify Your Email or Mobile No. and Password')
        return render(request, 'user_profile/login.html', {'form':form,
                                                            "message" : message,
                                                            })
"""CCRH Login Functionality - ends"""
     
     
"""CCRH Logout Functionality - starts"""     
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
"""CCRH Logout Functionality - ends"""


""" Dashboard functionality  - Starts"""
@login_required                
def dashboard(request):
    if request.method == 'GET':
        succes_message = request.session.pop('succes_message', None)
        return render(request, 'user_profile/dashboard.html', {'succes_message':succes_message,})
"""Dashboard functionality. - Ends"""
   
   
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

"""Registration profile step 1 starts here"""
def registration_step(request):
    if request.method == "GET":
        group_name=Group.objects.all()
        succes_message = request.session.pop('succes_msg', None)
        return render(request, 'user_profile/registration_step.html',{'group_name':group_name,
                                                                      'succes_message':succes_message})
    
    elif request.method == "POST":
        group_id = request.POST.get('added_role')
        request.session['group_id'] = group_id
        return HttpResponseRedirect(reverse_lazy('user_profile:profile_info'))
     
"""Registration Step2 Function Starts here"""
def registration_profile_info(request):
    if request.method == "GET":
#         form = RegistrationStep2()
        state=State.objects.filter(status_id=1)
        city=City.objects.filter(status_id=1)
        group_id = request.session.pop('group_id', None)
        succes_message = request.session.pop('succes_msg', None)
        return render(request, 'user_profile/registration_profile_info.html',{'group_id':group_id,
                                                                              'state':state,
                                                                              'city':city,
                                                                              'succes_message':succes_message})

    elif request.method == "POST":
        #Generating random password here
        random_string = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(8)])
        #Adding Data in user table
        if not User.objects.filter(email=request.POST.get('email')) and not  AdditionalProfile.objects.filter(mobile_no=request.POST.get('mobile_number')) .exists():
            user_id = User.objects.create_user(first_name=request.POST.get('first_name'),
                                          last_name = request.POST.get('last_name'),
                                          email = request.POST.get('email'),
                                          username = make_unique_username(request.POST.get('email')),
                                          password =random_string)
            if request.POST.get('sesion_group_id'):
                user_id.groups.add(request.POST.get('sesion_group_id'))
            elif request.POST.get('mbl_group_id'):
                user_id.groups.add(request.POST.get('mbl_group_id'))
            else:
                user_id.groups.add(request.POST.get('group_id'))
            #creating Additional Profile starts here
            AdditionalProfile.objects.create(user_id=user_id.id,
                                             mobile_no=request.POST.get('mobile_number') ,
                                             address_line1=request.POST.get('address_1') ,
                                             address_line2=request.POST.get('address_2'),
                                             state_id=request.POST.get('state_name') if request.POST.get('state_name') else None,
                                             city_id=request.POST.get('city_name') if request.POST.get('city_name') else None,
                                             pincode=request.POST.get('pincode') if request.POST.get('pincode') else None)
            #sending Email After saving starts
            subject = "Thanks for Registration in CCRH"
            if settings.SEND_MAIL_ALL_PLACE:
                to_email = request.POST.get('email')
                subject = "Thanks for Registration in CCRH"
                from_email, to = settings.ADMIN_EMAIL, [to_email]
                html_content = "Welcome to CCRH Portal Youer Passwrd {random_string} and User name {username} and Email {email}" .format(email=user_id.email,
                                                            username=user_id.username,
                                                            random_string=random_string)
                text_content = format_html(html_content)
                email = EmailMultiAlternatives(subject, text_content, from_email, to)
                email.content_subtype = 'html'
                email.send()
                #sending Email After saving ends
            request.session['succes_msg']=_('Registration has been created successfully')
            return HttpResponseRedirect(reverse_lazy('user_profile:registration_step'))
        else:
            already_exists=_('Mobile Number or Email already Exists')
            state=State.objects.filter(status_id=1)
            city=City.objects.filter(status_id=1)
            return render(request, "user_profile/registration_profile_info.html",{'first_name':request.POST.get('first_name'),
                                                                                  'state':state,
                                                                                  'city':city,
                                                                                  'sesion_group_id':request.POST.get('group_id'),
                                                                                  'mbl_group_id':request.POST.get('sesion_group_id'),
                                                                                  'middle_name':request.POST.get('middle_name'),
                                                                                  'last_name':request.POST.get('last_name'),
                                                                                  'email':request.POST.get('email'),
                                                                                  'address_line1':request.POST.get('address_1'),
                                                                                  'address_line2':request.POST.get('address_2'),
                                                                                  'mobile_number':request.POST.get('mobile_number'),
                                                                                  'state_id':int(request.POST.get('state_name')) if request.POST.get('state_name') else None,
                                                                                  'city_id':int(request.POST.get('city_name')) if request.POST.get('city_name') else None,
                                                                                  'pincode':request.POST.get('pincode') if request.POST.get('pincode') else None,
                                                                                  'message':already_exists,
                                                                  })
            
"""Registration Step3 Function Starts here"""
def registration_document_upload(request):
    if request.method == "GET":
        form = RegistrationStep3()
        return render(request, 'user_profile/registration_document_upload.html',{'form':form})
