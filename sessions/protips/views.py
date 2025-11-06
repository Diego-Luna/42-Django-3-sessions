from django.shortcuts import render

def index(request):
	"""Homepage for Life Pro Tips — uses anonymous name from context processor."""
	return render(request, 'protips/index.html')
