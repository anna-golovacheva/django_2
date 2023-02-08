from django import forms
from django.contrib.auth.forms import UserChangeForm, UsernameField, \
    PasswordResetForm, AuthenticationForm, SetPasswordForm

from base.forms import StyleFormMixin
from users.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class CustomEditUserForm(StyleFormMixin, UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Сохранить изменения'))

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'avatar',)
        field_classes = {'username': UsernameField}


class CustomUserCreationForm(StyleFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Зарегистрироваться'))

    class Meta:
        model = User
        fields = ('email', 'password', 'avatar',)
        # field_classes = {'username': UsernameField}


class CustomAuthenticationForm(StyleFormMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Войти'))

    class Meta:
        model = User


class CustomChangePasswordForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Сохранить'))


class CustomResetConfirmForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Изменить пароль'))


class CustomPasswordResetForm(StyleFormMixin, PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Сбросить пароль'))

    class Meta:
        model = User
