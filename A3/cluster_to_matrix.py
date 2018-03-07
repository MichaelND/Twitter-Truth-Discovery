"""
Michael Wang
March 7, 2018
Assignment 3
Convert a cluster of tweets into a sensing matrix
"""

import json

# Main
def main():
	sensing_matrix		= []

	cluster_tweets 	= open('cluster_tweets.txt', 'r')
	cluster_matrix 	= open('cluster_matrix.txt', 'w')

	#parse input tweets into sensing_matrix (list of dictionaries)
	for line in cluster_tweets:
		measured_variable 	= 0
		source				= 0
		source_list			= []

		measured_variable 	= line.split(':')
		measured_variable 	= measured_variable[0]
		source 				= line.split(':')
		source 				= source[1].split(',')

		for s in source:
			source_list.append(s.rstrip('\n'))

		# print(source_list)
		for source_id in source_list:
			new_dict = {}

			if new_dict.get(source_id) == None:
				new_dict[source_id] = []
			
			new_dict[source_id] = measured_variable
			sensing_matrix.append(new_dict)

	# print(sensing_matrix)

	#format sensing_matrix into cluster matrix file
	for line in sensing_matrix:
		for k, v in line.items():
			cluster_matrix.write(str(k) + ',' + str(v) + '\n')

	cluster_tweets.close()
	cluster_matrix.close()

#Start
if __name__ == '__main__':
	main()