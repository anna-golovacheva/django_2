import datetime
import pytz
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.views import LoginView, PasswordChangeView, \
    PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, \
    PasswordResetCompleteView
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView

from users.forms import CustomEditUserForm, CustomUserCreationForm, \
    CustomPasswordResetForm, CustomAuthenticationForm, \
    CustomChangePasswordForm, CustomResetConfirmForm
from users.models import User
from django.contrib.auth.hashers import make_password


def send_register_mail(message, email):
    send_mail(
        subject='активация',
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )


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
            password = form.data.get('password')
            self.object.set_password(password)
            self.object.token = make_password(self.object.password)[-15:]
            self.object.token_expired = datetime.datetime.now().astimezone() + datetime.timedelta(hours=72)
            self.object.is_active = False

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


# def confirm_new_generated_password(request):
#     current_user = User.objects.filter(email=request.GET.get('email')).first()
#     current_user.password = current_user.new_password
#     current_user.new_password = None
#     current_user.save()
#
#     return redirect(...)