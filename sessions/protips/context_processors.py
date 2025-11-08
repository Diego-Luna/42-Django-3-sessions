import time
import random
from django.conf import settings


def anonymous_name(request):
	"""
	Ensure the user has an anonymous name stored in the session for a TTL (42s).
	"""

	# If the user is authenticated, prefer their username instead of an anonymous name
	user = getattr(request, 'user', None)
	if user and user.is_authenticated:
		return {'anonymous_name': user.get_username()}

	now = int(time.time())
	name = request.session.get('anon_name')
	ts = request.session.get('anon_name_ts')
	ttl = getattr(settings, 'ANONYMOUS_NAME_TTL', 42)

	if not name or not ts or (now - int(ts) >= int(ttl)):
		names = getattr(settings, 'ANONYMOUS_NAMES', None)
		if not names:
			return {'anonymous_name': "error-no-names-configured"}
		new_name = random.choice(names)
		request.session['anon_name'] = new_name
		request.session['anon_name_ts'] = now
		name = new_name

	return {'anonymous_name': name}
