"""
Michael Wang
February 19, 2018
Assignment 2
"""

import tweepy
import json
import itertools

#Jaccard Distance Function
def Distance(A, B):
	#calculate intersection, union, and distance of A and B
	intersection	= len(A.intersection(B))
	union			= len(A.union(B))
	distance		= 1 - (intersection / union)

	return distance

def KMeans(centroid_words, tweet_words):
	#K-Means algorithm
	#Go through all the tweets not in centroid, find the distance between each tweet
	#and each centroid tweet, find the smallest distance and cluster put that tweet
	#in a cluster near that id

	distance			= 1
	best_tweet_key		= 0
	best_centroid_key	= 0
	centroid_clusters	= {}

	#initialize dictionary of lists where centroid tweet id is the key
	for centroid_k, centroid_v in centroid_words.items():
		centroid_clusters[centroid_k] = []

	for tweet_k, tweet_v in tweet_words.items():
		for centroid_k, centroid_v in centroid_words.items():
			#find the smallest distance to centroid point and update values
			if Distance(tweet_v, centroid_v) < distance: 
				distance 			= Distance(tweet_v, centroid_v)
				best_centroid_key 	= centroid_k
				best_tweet_key		= tweet_k

		centroid_clusters[best_centroid_key].append(tweet_k)
		distance = 1

	return centroid_clusters

def Calculate_New_Centroids(centroid_clusters, all_words, K):
	#go through each of the tweets in clusters, assign each id as centroid, calculate distance from each and every other tweet
	#and average the distance, then compare all centroids, whichever has the smallest distance, make new centroid of one cluster

	next_centroids			= set()
	distance				= 0
	new_centroid_clusters	= {}
	avg_centroid_distances	= {}
	cluster					= 0 
	len_v					= 0 #number of tweet ids for a given centroid key

	for x in range(0, K):
		new_centroid_clusters[x]	= []
		avg_centroid_distances[x]	= []

	#Construct replacement dictionary for old centroid clusters with key:value being numbers 0-K:tweet_ids
	for k, v in centroid_clusters.items():
		for tweet_id in v:
			new_centroid_clusters[cluster].append(tweet_id)

		new_centroid_clusters[cluster].append(k)
		cluster += 1

	#iterate through values of tweet_ids and calculate average Jaccard Distance 
	for k, v in new_centroid_clusters.items():
		len_v = len(v)
		for x, y in itertools.permutations(v, 2):
			distance = distance + Distance(all_words[x], all_words[y])
			len_v -= 1
			if len_v == 1: #one round of permutations of one number to the rest passed
				len_v = len(v) #reset length iterator
				distance = distance / (len_v - 1) #compute average distance
				avg_centroid_distances[k].append((x, distance))
				distance = 0 #reset distances

	#Find the tweet id with the smallest distance within each of the K clusters
	smallest_distance 	= 1
	new_centroid_id 	= 0
	for k, v in avg_centroid_distances.items():
		for tweet_pair in v:
			if tweet_pair[1] < smallest_distance:
				smallest_distance 	= tweet_pair[1]
				new_centroid_id 	= tweet_pair[0]

		smallest_distance = 1
		next_centroids.add(new_centroid_id) #Add to set of new centroids

	return next_centroids

# Main
def main():
	centroid_ids		= set() 
	next_centroids		= set()
	prev_centroids 		= set()
	centroid_clusters	= {}
	tweet_info			= []
	tweet_words			= {}
	centroid_words		= {}
	all_words			= {}
	K					= 0

	############## load in file information ################################

	result_file = open('results.txt', 'w')

	for line in open('tweets.json', 'r'):
		tweet_info.append(json.loads(line))

	for line in open('seeds.txt', 'r'):
		centroid_ids.add(line.strip(' ,\n'))

	K = len(centroid_ids)

	############## loop until centroids don't move #########################

	while centroid_ids != prev_centroids:
		prev_centroids = centroid_ids
		print('Computing new centroids')

		#Create dictionaries for tweets in centroid and tweets not in centroid
		for tweet in tweet_info:
			new_set = set()
			if str(tweet['id']) in prev_centroids:
				for word in tweet['text'].split():
					if word not in new_set: #remove duplicate words
						new_set.add(word)

				centroid_words[tweet['id']]	= new_set 	#list of set of all tweets in centroid
				all_words[tweet['id']]		= new_set 
			else:
				for word in tweet['text'].split():
					if word not in new_set: #remove duplicate words
						new_set.add(word)

				tweet_words[tweet['id']] 	= new_set 		#list of set of all tweets not in centroid
				all_words[tweet['id']]		= new_set 

		####### Perform K-Means on the centroids and tweets ################
		centroid_clusters = KMeans(centroid_words, tweet_words)

		####### Calculate New Centroids from a cluster of tweets ############
		centroid_ids = {}
		centroid_ids = Calculate_New_Centroids(centroid_clusters, all_words, K)

	############## Write final centroid clusters to file#####################

	for k, v in centroid_clusters.items():
		result_file.write(str(k) + ': ' + str(v) + '\n')

	result_file.close()

#Start
if __name__ == '__main__':
	main()
