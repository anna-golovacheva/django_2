from django.conf import settings

import datetime
import pytz

from django.contrib.auth.views import LoginView, PasswordChangeView, \
    PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, \
    PasswordResetCompleteView
from django.views.generic import UpdateView, CreateView

from users.models import User

from users.forms import CustomEditUserForm, CustomUserCreationForm, \
    CustomPasswordResetForm, CustomAuthenticationForm, \
    CustomChangePasswordForm, CustomResetConfirmForm

from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from app.services import send_register_mail, set_registration


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = CustomAuthenticationForm


class CustomRegisterView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:continue_registration')

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            self.object = set_registration(form, self.object)
            self.object.save()

            send_register_mail(
                message=f'Чтобы завершить регистрацию, перейдите по ссылке:\nhttp://localhost:8000/users/activate/{self.object.token}/',
                email=self.object.email
            )

        return super().form_valid(form)


class UserEditProfileView(UpdateView):
    model = User
    template_name = 'users/profile.html'
    form_class = CustomEditUserForm
    success_url = reverse_lazy('app:index')

    def get_object(self, queryset=None):
        return self.request.user


class CustomPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('app:index')
    template_name = 'users/change_password.html'
    form_class = CustomChangePasswordForm


def user_activation(request, token):
    user = User.objects.filter(token=token).first()

    if user:
        now = datetime.datetime.now((pytz.timezone(settings.TIME_ZONE)))
        if user.token_expired > now:
            user.is_active = True
            user.token = None
            user.token_expired = None
            user.save()

            return redirect(to='/users/')

        user.delete()
    return redirect(to='/users/registration_failed')


def registration(request):
    return render(request, 'users/continue_register.html')


def registration_failed(request):
    return render(request, 'users/registration_failed.html')


class CustomPasswordResetView(PasswordResetView):
    template_name = 'users/reset_password.html'
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('users:password_reset_done')
    email_template_name = 'users/email_reset.html'
    from_email = settings.EMAIL_HOST_USER


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')
    form_class = CustomResetConfirmForm


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/reset_done.html'


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/reset_complete.html'
