from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.urls import reverse
from .forms import RegistrationForm, LoginForm, TipForm
from .models import Tip
from django.views.decorators.http import require_POST


User = get_user_model()


@require_POST
def tip_vote(request, tip_id):
	if not request.user.is_authenticated:
		return redirect('protips:login')

	tip = Tip.objects.get(id=tip_id)
	value = int(request.POST.get('value'))
	
	
	tip.vote(request.user, value)
	
	return redirect('protips:index')

@require_POST
def tip_delete(request, tip_id):
	if not request.user.is_authenticated:
		return redirect('protips:login')

	tip = Tip.objects.get(id=tip_id)
	if tip.author == request.user or request.user.has_perm('protips.delete_tip'):
		tip.delete()
	
	return redirect('protips:index')

def index(request):

	tips = Tip.objects.all()
	if request.user.is_authenticated:
		if request.method == 'POST':
			form = TipForm(request.POST)
			if form.is_valid():
				content = form.cleaned_data['content']
				Tip.objects.create(content=content, author=request.user)
				return redirect(reverse('protips:index'))
		else:
			form = TipForm()

		return render(request, 'protips/index.html', {'tips': tips, 'form': form})
	else:
		return render(request, 'protips/index.html', {'tips': tips})


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
	# * yes is only one line
	logout(request)
	return redirect('protips:index')
