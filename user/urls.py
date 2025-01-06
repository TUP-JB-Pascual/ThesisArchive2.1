from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

#USE ONLY ON DEVELOPMENT
from django.conf import settings
from django.conf.urls.static import static
#USE ONLY ON DEVELOPMENT


urlpatterns = [
    path('account-list/', views.UserListView, name='account_list'),
    path('account-detail/<int:pk>', views.UserManageView, name='account_detail'),
    path('account-detail/<int:pk>/deactivate', views.DeactivateUser, name='deactivate_user'),
    path('account-detail/<int:pk>/activate', views.ActivateUser, name='activate_user'),
    path('account-detail/<int:pk>/revoke-admin', views.ChangeAccTypeToStudent, name='revoke_admin'),
    path('account-detail/<int:pk>/grant-admin', views.ChangeAccTypeToAdmin, name='grant_admin'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('registration/', views.UserRegisterView, name='user_registration'),
    path('verify-email/<str:uidb64>/<str:token>/', views.VerifyEmail, name='verify_email'),
    path('user-profile/', views.UserProfile, name='user_profile'),
    path('update-profile/', views.UserUpdateProfile, name='update_profile'),
    path('change-password/', views.UserChangePassword, name='change_password'),
    path('restricted-page/', views.RestrictedPage, name='restricted_page'),

    path('forgot-password/', views.CustomPasswordResetView.as_view(), name='forgot_password'),
    path('password-reset-done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    # user profile
        # change pass (All User)
        # forgot password (All User)
        # add ID # as improvement
]
