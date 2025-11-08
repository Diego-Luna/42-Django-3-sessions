from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.urls import reverse
from .forms import RegistrationForm, LoginForm


User = get_user_model()


def index(request):
	"""Homepage for Life Pro Tips — uses anonymous name from context processor or username."""
	return render(request, 'protips/index.html')


def register_view(request):
	if request.user.is_authenticated:
		return redirect('protips:index')

	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = User.objects.create_user(username=username, password=password)
			login(request, user)
			return redirect('protips:index')
	else:
		form = RegistrationForm()

	return render(request, 'protips/register.html', {'form': form})


def login_view(request):
	if request.user.is_authenticated:
		return redirect('protips:index')

	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect('protips:index')
			else:
				form.add_error(None, 'Invalid username or password.')
	else:
		form = LoginForm()

	return render(request, 'protips/login.html', {'form': form})


def logout_view(request):
	# Allow logout via GET for simplicity (exercise expects a link)
	logout(request)
	return redirect('protips:index')
