from django.test import TestCase, Client

def init_client(user):

	client = Client()
	client.login(username=user.username, password="lzz")
	s = client.session
	s['cur_user_id'] = user.id
	s.save()
	return client