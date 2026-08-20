from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Kullanıcı adı'
        self.fields['password'].widget.attrs['placeholder'] = 'Şifre'


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Kullanıcı adı'
        self.fields['password1'].widget.attrs['placeholder'] = 'Şifre'
        self.fields['password1'].help_text = 'En az 8 karakter, tamamen sayısal olmasın.'
        self.fields['password2'].widget.attrs['placeholder'] = 'Şifre (tekrar)'
        self.fields['password2'].help_text = None
