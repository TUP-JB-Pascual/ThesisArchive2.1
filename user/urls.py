from django.urls import path
from . import views

#USE ONLY ON DEVELOPMENT
from django.conf import settings
from django.conf.urls.static import static
#USE ONLY ON DEVELOPMENT


urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('registration/', views.UserRegisterView, name='user_registration'),
    path('verify-email/<str:uidb64>/<str:token>/', views.VerifyEmail, name='verify_email'),
    path('user-profile/', views.UserProfile, name='user_profile'),
    path('update-profile/', views.UserUpdateProfile, name='update_profile'),
    path('change-password/', views.UserChangePassword, name='change_password'),
    path('forgot-password/', views.UserForgotPassword, name='forgot_password'),
    # user profile
        # change pass (All User)
        # forgot password (All User)
        # add ID # as improvement
]
