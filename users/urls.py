from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView, PasswordChangeView
from django.urls import path
from users.apps import UsersConfig
from users.views import CustomLoginView, UserEditProfileView, \
    CustomRegisterView, CustomPasswordChangeView, user_activation, \
    registration, registration_failed, CustomPasswordResetView, \
    CustomPasswordResetConfirmView, CustomPasswordResetDoneView, \
    CustomPasswordResetCompleteView

app_name = UsersConfig.name

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', login_required(UserEditProfileView.as_view()), name='profile'),
    path('register/', CustomRegisterView.as_view(), name='register'),
    path('password/', CustomPasswordChangeView.as_view(), name='reset_password'),
    path('activate/<str:token>/', user_activation, name='activate'),
    path('register_continue/', registration, name='continue_registration'),
    path('register_failed/', registration_failed, name='registration_failed'),
    path('password/reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password/reset/<uidb64>/confirm/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password/reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password/reset/complete/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

]