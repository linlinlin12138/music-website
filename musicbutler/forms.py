from django import forms
from django.contrib.auth.models import User
from .models import Comments,FavouriteList,Exist


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['content']

class ListForm(forms.ModelForm):
    class Meta:
        model = FavouriteList
        fields = ['name']

class AddToFavoritesForm(forms.Form):
    favorite_list = forms.ModelChoiceField(queryset=FavouriteList.objects.none(), empty_label=None)
    song_id = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['favorite_list'].queryset = FavouriteList.objects.filter(user=user)

    class Meta:
        model=FavouriteList
        fields=['name']
    '''def save(self, user):
        favorite_list = self.cleaned_data['favorite_list']
        song_id = self.cleaned_data['song_id']
        exist,created = Exist.objects.get_or_create(list=favorite_list.list_id, user=user.id, song=song_id)'''

class SearchForm(forms.Form):
    query = forms.CharField()
