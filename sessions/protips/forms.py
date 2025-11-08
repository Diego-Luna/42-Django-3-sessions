from django import forms
from django.contrib.auth import get_user_model


User = get_user_model()


class RegistrationForm(forms.Form):
	username = forms.CharField(
		label='Username',
		max_length=150,
		widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'})
	)
	password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
	password_confirm = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

	def clean_username(self):
		username = self.cleaned_data.get('username')
		if User.objects.filter(username=username).exists():
			raise forms.ValidationError('This username is already taken.')
		return username

	def clean(self):
		cleaned = super().clean()
		p = cleaned.get('password')
		pc = cleaned.get('password_confirm')
		if p and pc and p != pc:
			raise forms.ValidationError('Passwords do not match.')
		return cleaned


class LoginForm(forms.Form):
	username = forms.CharField(label='Username', max_length=150,
		widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
	password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
