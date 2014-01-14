from bs4 import BeautifulSoup
import re
import urllib2
from rango.models import TvShows, Episode, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from sendEmail import send_email
import re

""" 
redditFile = urllib2.urlopen("http://www.reddit.com")
redditHtml = redditFile.read()
redditFile.close()
 
soup = BeautifulSoup(redditHtml)
redditAll = soup.find_all("a")
for links in soup.find_all('a'):
    print (links.get('href')) """

def getLatestEpisodes():

	showsgoHtmls = []
	showsgoFile = urllib2.urlopen("http://showsgo.com/")
	showsgoHtml = showsgoFile.read()
	showsgoHtmls.append(showsgoHtml)
	showsgoFile.close()

	# for i in range(2, 11):
	# 	text = "http://showsgo.com/page/%d"%i
	# 	#print(text)
	# 	showsgoFile = urllib2.urlopen(text)
	# 	showsgoHtml = showsgoFile.read()
	# 	showsgoHtmls.append(showsgoHtml)
	# 	showsgoFile.close()	

	# soup = BeautifulSoup(showsgoHtml)

	for page in showsgoHtmls:
		soup = BeautifulSoup(page)
		for links in soup.ul.find_all('li'):
			show = None
			title = None
			stream = None
			image = None
			for url in links.find_all('div', {'class' : 'cover'}):
				title = url.a.get('title')
				stream = url.a.get('href')	
				image = url.a.find('img')['src']
			
			for url in links.find_all('div', {'class' : 'postcontent'}):
<<<<<<< HEAD
				show = url.a.get('title').split('Full Episodes')[0]
=======
				show = url.a.get('title').split(' Full Episodes')[0]
>>>>>>> 28c67df61b0d09a43ec839b3403e7e355ef5f291
			
			if title is not None:
				p = None
				if (TvShows.objects.filter(show_name=show).count() < 1):
					p = TvShows(show_name=show, picture_link=image)
					p.save()	
				else:
					p = TvShows.objects.get(show_name=show)											
<<<<<<< HEAD

				if (Episode.objects.filter(show_link=stream).count() < 1):
				 		a = Episode(show=p, show_link=stream, season_episode=title)
				 		a.save()
	
getLatestEpisodes()
=======

				if (Episode.objects.filter(show_link=stream).count() < 1):
				 		a = Episode(show=p, show_link=stream, season_episode=title)
				 		a.save()
	
getLatestEpisodes()

# TESTING CREATING FAKE USERS
# USERNAME: USMAN PW:USMAN
# USERNAME: MICHAEL PW:MICHAEL

if authenticate(username='usman', password='usman')==None:
	a = User.objects.create_user(username='usman', password='usman', email='uehtesham90@gmail.com')
	a.save()
	b = UserProfile(user_id=a.id)
	b.save()
else:
	a = authenticate(username='usman', password='usman')

if authenticate(username='michael', password='michael')==None:
	c = User.objects.create_user(username='michael', password='michael', email='mickeyho92@gmail.com', last_name='15146210791')
	d = UserProfile(user_id=c.id)
	c.save()
	d.save()
else:
	c = authenticate(username='michael', password='michael')

for show in TvShows.objects.all():
	show.users.add(a)
	b = UserProfile.objects.filter(user=a)[0]
	b.show_list.add(show)
	show.users.add(c)
	d = UserProfile.objects.filter(user=c)[0]
	d.show_list.add(show)
>>>>>>> 28c67df61b0d09a43ec839b3403e7e355ef5f291

print len(TvShows.objects.all())

print len(Episode.objects.all())

for i in Episode.objects.all():
	if i.sent == False:
<<<<<<< HEAD
		to = i.show.getUsers()
		s = 'Here is link to the latest episode of ' + i.getSeasonAndEpisode() +' : \n' + i.getShowLink()
		send_email(to,'Shows Alert Update', s)
		i.sent = True
		i.save()
=======
		for u in i.show.users.all(): # Loop through all the users and use their emails
			p = UserProfile.objects.filter(user=u)[0]
			if p.email_notification: # Check if email_notification is activated
				to = u.email
				s = 'Here is link to the latest episode of ' + i.getSeasonAndEpisode() +' : \n' + i.getShowLink()
				send_email(to,'Shows Alert Update', s)
				i.sent = True
				i.save()
>>>>>>> 28c67df61b0d09a43ec839b3403e7e355ef5f291
