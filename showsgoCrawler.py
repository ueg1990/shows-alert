import sys; sys.path.append('/Users/michaelho/shows-alert/')
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

	for i in range(2, 11):
		text = "http://showsgo.com/page/%d"%i
		#print(text)
		showsgoFile = urllib2.urlopen(text)
		showsgoHtml = showsgoFile.read()
		showsgoHtmls.append(showsgoHtml)
		showsgoFile.close()

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
				show = url.a.get('title').split(' Full Episodes')[0]
							
			if title is not None:
				p = None
				if (TvShows.objects.filter(show_name=show).count() < 1):
					p = TvShows(show_name=show, picture_link=image)
					p.save()	
				else:
					p = TvShows.objects.get(show_name=show)											


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
	b.newuser = False
	b.save()
else:
	a = authenticate(username='usman', password='usman')

# if authenticate(username='michael', password='michael')==None:
# 	c = User.objects.create_user(username='michael', password='michael', email='mickeyho92@gmail.com', last_name='15146210791')
# 	d = UserProfile(user_id=c.id)
# 	d.newuser = False
# 	c.save()
# 	d.save()
# else:
# 	c = authenticate(username='michael', password='michael')

for show in TvShows.objects.all():
	show.users.add(a)
	b = UserProfile.objects.get(user=a)
	b.show_list.add(show)
	# show.users.add(c)
	# d = UserProfile.objects.get(user=c)
	# d.show_list.add(show)


print len(TvShows.objects.all())

print len(Episode.objects.all())

for u in UserProfile.objects.all():
	if u.newuser:
		for show in u.show_list.all():
			latest_episode = Episode.objects.filter(show=show).order_by('-creation_date')[:1]
			latest_episode = latest_episode[0]
			if u.email_notification: # EMAIL
				to = u.user.email
				s = 'Here is link to the latest episode of ' + latest_episode.getSeasonAndEpisode() +' : \n' + latest_episode.getShowLink()
				send_email(to,'Shows Alert Update', s)
		u.newuser = False
		u.save()

for i in Episode.objects.all():
	if i.sent == False:
		for u in i.show.users.all(): # Loop through all the users and use their emails
			p = UserProfile.objects.get(user=u) # Get corresponding UserProfile 
			if p.email_notification: # EMAIL
				to = u.email
				s = 'Here is link to the latest episode of ' + i.getSeasonAndEpisode() +' : \n' + i.getShowLink()
				send_email(to,'Shows Alert Update', s)
				i.sent = True
				i.save()
			if p.sms_notification: # SMS
				a = 0



