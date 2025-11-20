from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth import authenticate, login, logout, get_user_model # type: ignore
from django.urls import reverse # type: ignore
from .forms import RegistrationForm, LoginForm, TipForm
from .models import Tip
from django.views.decorators.http import require_POST # type: ignore

User = get_user_model()


@require_POST
def tip_vote(request, tip_id):
	if not request.user.is_authenticated:
		return redirect('protips:login')

	tip = Tip.objects.get(id=tip_id)
	value = int(request.POST.get('value'))
	
	if value == -1 and not (request.user.has_downvote_permission() or tip.author == request.user):
		return redirect('protips:index')
	
	tip.vote(request.user, value)
	return redirect('protips:index')

@require_POST
def tip_delete(request, tip_id):
	if not request.user.is_authenticated:
		return redirect('protips:login')

	tip = Tip.objects.get(id=tip_id)
	if tip.author == request.user or request.user.has_deletion_permission():
		tip.delete()

	return redirect('protips:index')

def index(request):

	# Optimization: Fetch all tips with their authors to avoid N+1 queries.
	tips = Tip.objects.select_related('author').all()
	authors = {tip.author for tip in tips}
	if request.user.is_authenticated:
		authors.add(request.user)

	# Calculate reputation for all relevant authors in a single query
	author_reputations = {
		user.id: user.calculate_reputation()
		for user in authors
	}

	# Attach reputation to each author object to avoid lazy queries in template
	for tip in tips:
		tip.author.reputation = author_reputations.get(tip.author.id, 0)
	
	if request.user.is_authenticated:
		request.user.reputation = author_reputations.get(request.user.id, 0)


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
			# Best practice: specify the backend.
			user.backend = 'django.contrib.auth.backends.ModelBackend'
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
