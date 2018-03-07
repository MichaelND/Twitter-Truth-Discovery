"""
Michael Wang
January 26, 2018
Assignment 1
"""
############### Authentication ###################
import tweepy

consumer_key 		= 'h1jdyvrYixMRp82nwPlhnDO2L'
consumer_secret 	= 'GfQXpGKe8D8RdjynamTTQoQogB7rSmu3AoGN2mmUMbalM5bhpm'
access_token 		= '1713927985-BbQV8KN4VOLoHwkhiRS1MPs4c6xqlMg6VXAPTuw'
access_token_secret = 'G5Y6k5brWzQszu0SxhDGUYeAmY9fy0b0w1l27MhTMUBVq'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api  = tweepy.API(auth)
user = api.me()

user_ids = [34373370, 26257166, 12579252]
keywords = ["Indiana", "weather"]
regions  = [-86.33, 41.63, -86.20, 41.74]

################## Part 1 ########################

f = open('Part1.txt', 'w')

for index, item in enumerate(user_ids):
	u = api.get_user(item)

	f.write('USER ID: ' + str(item) + '\n')
	f.write('Screen Name:' + u.screen_name + '\n')
	f.write('User Name:' + u.name + '\n')
	f.write('User Location:' + u.location + '\n')
	f.write('User Description:' + u.description + '\n')
	f.write('The Number of Followes:' + str(u.followers_count) + '\n')
	f.write('The Number of Friends:' + str(u.friends_count) + '\n')
	f.write('The Number of Statuses:' + str(u.statuses_count) + '\n')
	f.write('User URL:' + u.url + '\n\n')

f.close()
print("Part1: Complete")

# # ################# Part 2 #########################

f = open('Part2.txt', 'w')

for index, item in enumerate(user_ids):
	friends_list = api.friends_ids(item)
	followers_list = api.followers_ids(item)

	f.write('User ID: ' + str(item) + '\n')
	f.write('The Friends List:\n')

	for friend in friends_list[:20]:
		u = api.get_user(friend)
		f.write(u.screen_name + '\n')

	f.write('\nThe Followers List:\n')

	for follower in followers_list[:20]:
		u = api.get_user(follower)
		f.write(u.screen_name + '\n')

	f.write('\n')

f.close()
print("Part2: Complete")

################# Part 3.1 #######################

class MyStreamListener(tweepy.StreamListener):
	def __init__(self, api=None):
		super(MyStreamListener, self).__init__()
		self.tweet_count = 0

	def on_status(self, status):
		self.tweet_count += 1
		if self.tweet_count < 51: #only record up to 50 tweets
			f.write('Tweet #' + str(self.tweet_count) + ' ' + status.text + '\n')
			return True
		else:
			return False

f = open('Part3.1.txt', 'w')

MyStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=MyStreamListener)

for word in keywords:
	myStream.filter(track=keywords)

print("Part3.1: Complete")

f.close()

################# Part 3.2 #######################

class MyStreamListener(tweepy.StreamListener):
	def __init__(self, api=None):
		super(MyStreamListener, self).__init__()
		self.tweet_count = 0

	def on_status(self, status):
		self.tweet_count += 1
		if self.tweet_count < 51: #only record up to 50 tweets
			f.write('Tweet #' + str(self.tweet_count) + ' ' + status.text + '\n')
			return True
		else:
			return False

f = open('Part3.2.txt', 'w')

MyStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=MyStreamListener)

myStream.filter(locations=regions)

print("Part3.2: Complete")

f.close()
