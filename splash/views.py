from django.shortcuts import render
from django.http import HttpResponse
from facepy import GraphAPI

base = '384063111614994/feed' # base URL

# tries to judge is message is actually for a study post
def judicator(message):
	score = 0
	if '$' in message:
		score += 1
	if 'participat' in message or 'participant' in message: 
		score += 1
	if 'experiment' in message:
		score += 0.5

	if score >= 2:
		return True
	else:
		return False

# Create your views here.
def index(request):
	# if the user is logged in, access the graph API
	if request.user.is_authenticated():
		social = request.user.social_auth.get(provider='facebook')
		access_token = social.extra_data['access_token']
		graph = GraphAPI(access_token)

		# gets indicated page number unless there isn't one
		num = request.GET.get('page')
		if num is None or int(num) < 0:
			num = 0
		else:
			num = int(num)

		nextpg = num + 1
		prevpg = num - 1

		data = graph.get(base) # gets base

		while num > 0:
			# gets the messages of the first 25 posts and address for next page
			try:
				nxt = data['paging']['next'][32:] # GET address of next page
				data = graph.get(nxt)
				num -= 1
			except KeyError:
				nextpg = None
				break
			

		messages = [post for post in data['data'] if 'message' in post and judicator(post['message'])]

		return render(request, 'index.html', {'user': request.user, 'posts': messages, 'previous': prevpg, 'next': nextpg})

	else:
		return render(request, 'index.html', {'user': request.user})


