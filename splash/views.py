from django.shortcuts import render
from django.http import HttpResponse
from facepy import GraphAPI

# Create your views here.
def index(request):
	# if the user is logged in, access the graph API
	if request.user.is_authenticated():
		social = request.user.social_auth.get(provider='facebook')
		access_token = social.extra_data['access_token']
		graph = GraphAPI(access_token)

		# gets the messages of the first 25 posts
		data = graph.get('384063111614994/feed')
		messages = [post for post in data['data']]

		return render(request, 'index.html', {'user': request.user, 'posts': messages})

	else:
		return render(request, 'index.html', {'user': request.user})