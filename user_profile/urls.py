from django.urls import path, re_path
from user_profile import views as user_profile_views
from django.contrib.auth.views import PasswordResetConfirmView,PasswordResetCompleteView, PasswordResetView
from user_profile.forms import CustomSetPasswordForm, PasswordResetFormUnique, CustomPasswordChangeForm

app_name="user_profile"

urlpatterns = [
    path('login/', user_profile_views.login_view, name="login"),
    path('logout/', user_profile_views.logout_view, name='logout'),
    path('dashboard/', user_profile_views.dashboard, name='dashboard'),
    path('change_password/', user_profile_views.change_password, name='change_password'),
    path('forget_password/', user_profile_views.password_forgot, name='forget_password'),
    path('password-forgot/', user_profile_views.password_forgot, name='password_forgot'),
    #On click of password reset link, displaying a form to submit passwords.
    path('password_reset_<uidb64>_<token>/',PasswordResetConfirmView.as_view(
                                            form_class=CustomSetPasswordForm,
                                            template_name='user_profile/password_reset_confirm.html',
                                            success_url='/reset/done/'),
                                            name='password_reset_confirm'),
    #After password resetting done redirecting to a page having login link.
    path('reset/done/', PasswordResetCompleteView.as_view(
                                                template_name='user_profile/password_reset_complete.html'
                                                ), name='password_reset_complete'),
    ]