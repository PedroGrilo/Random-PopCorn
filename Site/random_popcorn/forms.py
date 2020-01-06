from bootstrap_modal_forms.forms import BSModalForm
from django import forms
from django.contrib.auth.forms import authenticate, get_user_model
from django_tables2 import tables

from .models import Movie

User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('This username does not exist')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect password')
            if not user.is_active:
                raise forms.ValidationError('This username is not active')
        return super(UserLoginForm, self).clean()


class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(label='Username')
    email = forms.EmailField(label='Email address')
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    birth_date = forms.CharField(widget=forms.DateInput)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password2',
            'birth_date'
        ]

    def clean(self, *args, **kwargs):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        email = self.cleaned_data.get('email')

        if password != password2:
            raise forms.ValidationError("Passwords do not match !")
        email_compare = User.objects.filter(email=email)
        if email_compare.exists():
            raise forms.ValidationError(
                "This email has already been registered")
        return super(UserRegisterForm, self).clean()


class AddMovieTable(tables.Table):
    selection = tables.columns.CheckBoxColumn(accessor='pk')

    class Meta:
        model = Movie
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = ['id', 'title', 'release_date', 'rating_imdb',]
        attrs = {"id": "tableMovies"}


class MovieForm(BSModalForm):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'release_date', 'rating_imdb', ]
