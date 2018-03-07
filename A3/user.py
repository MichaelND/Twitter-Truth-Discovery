"""
Michael Wang
March 7, 2018
Assignment 3
Take a sensing matrix and output the estimation results of whether 
each measure variable is true or not
"""

import random
import operator

# Main
def main():
	input_dict				= {}
	input_key, input_value	= 0, 0
	total_var, total_src	= 0, 0
	counter, i, j			= 0, 0, 0
	Atj, Btj				= 0, 0
	s, a, b, Z, h, t, K, d	= {}, {}, {}, {}, {}, {}, {}, {}
	totalZ, obsZ			= 0, 0
	matrix					= {}
	value_d					= ""

	############## load in file information #################################
	file 			= input("Enter the name of the file you want to test: ")
	input_matrix 	= open(file, 'r')
	value_d 		= input("Enter 1 for Part1 (d is random), Enter 2 for Part2 (d = 0.5): ")

	for line in input_matrix:
		input_key 					= line.split(',')[0].rstrip()
		input_dict[int(input_key)]	= set()
		matrix[int(input_key)]		= {}

	input_matrix.seek(0)

	for line in input_matrix:
		input_key	= line.split(',')[0].rstrip()
		input_value	= line.split(',')[1].rstrip()

		#Adjust number of total measured variables and sources
		if int(input_value) > int(total_var):
			total_var = int(input_value)
		if int(input_key) > int(total_src):
			total_src = int(input_key)

		input_dict[int(input_key)].add(int(input_value))

	input_matrix.close()

	############## calculate si, ai, bi, d, matrix ##########################
	#If we are doing part2, the sources will not be numerical so loop through keys
	#rather than iterative approach

	if int(value_d) == 2:
		for k, v in input_dict.items():
			reports_from_si = len(v)
			s[k] = float(reports_from_si/total_var)
			K[k] = len(v)
	else:
		for i in range(1, total_src + 1):
			reports_from_si = len(input_dict[i])
			s[i] = float(reports_from_si/total_var)
			K[i] = len(input_dict[i])

	if int(value_d) == 2:
		for k, v in input_dict.items():
			a[k] = s[k]
			b[k] = s[k] * 0.5
			for j in range(1, total_var + 1):
				if j in v:
					matrix[k][j] = 1
				else:
					matrix[k][j] = 0
	else:
		for i in range(1, total_src + 1):
			a[i] = s[i]
			b[i] = s[i] * 0.5
			for j in range(1, total_var + 1):
				if j in input_dict[i]:
					matrix[i][j] = 1
				else:
					matrix[i][j] = 0

	if int(value_d) == 1:
		d = random.random()
	elif int(value_d) == 2:
		d = 0.5
	else:
		d = random.random()

	############## Perform EM algorithm #####################################
	#If we are doing part2, the sources will not be numerical so loop through keys
	#rather than iterative approach
	
	if int(value_d) == 1:
		while counter < 20:
			counter += 1
			j = 1
			while j < total_var + 1:
				i = 1
				Atj = 1
				Btj = 1
				while i < total_src + 1:
					Atj *= pow(a[i], matrix[i][j]) * pow((1-a[i]), (1-matrix[i][j]))
					Btj *= pow(b[i], matrix[i][j]) * pow((1-b[i]), (1-matrix[i][j]))
					i += 1
				Z[j] = (Atj * d)/float(Atj*d+Btj*(1-d))
				j += 1

			#Calculate total Z
			for var in range(1, total_var + 1):
				totalZ += Z[var]

			#update a[i], b[i], d[i]
			i2 = 1
			while i2 < total_src + 1:
				#Calculate observed Z
				for var in range(1, total_var + 1):
					if var in input_dict[i2]:
						obsZ += Z[var]
				try:
					a[i2] = obsZ / float(totalZ)
				except ZeroDivisionError:
					a[i2] = 0

				try:
					b[i2] = (K[i2] - obsZ) / float(total_var - totalZ)
				except ZeroDivisionError:
					b[i2] = 0

				i2 += 1
				obsZ = 0

			d = float(totalZ) / total_var
			totalZ = 0

		#Calculate h[j]
		for j in range(1, total_var + 1):
			if Z[j] >= 0.5:
				h[j] = 1
			else:
				h[j] = 0
	else:
		while counter < 20:
			counter += 1
			j = 1
			while j < total_var + 1:
				Atj = 1
				Btj = 1
				for k, v in input_dict.items():
					Atj *= pow(a[k], matrix[k][j]) * pow((1-a[k]), (1-matrix[k][j]))
					Btj *= pow(b[k], matrix[k][j]) * pow((1-b[k]), (1-matrix[k][j]))
				Z[j] = (Atj * d)/float(Atj*d+Btj*(1-d))
				j += 1

			#Calculate total Z
			for var in range(1, total_var + 1):
				totalZ += Z[var]

			#update a[i], b[i], d[i]
			for k, v in input_dict.items():
				#Calculate observed Z
				for var in range(1, total_var + 1):
					if var in v:
						obsZ += Z[var]
				try:
					a[k] = obsZ / float(totalZ)
				except ZeroDivisionError:
					a[k] = 0

				try:
					b[k] = (K[k] - obsZ) / float(total_var - totalZ)
				except ZeroDivisionError:
					b[k] = 0

				obsZ = 0

			d = float(totalZ) / total_var
			totalZ = 0

		#Calculate h[j]
		for j in range(1, total_var + 1):
			if Z[j] >= 0.5:
				h[j] = 1
			else:
				h[j] = 0

	#Calculate source reliability t[i] (Seems like we don't use this)
	# for i in range(1, total_src + 1):
	# 	t[i] = (a[i] * d) / s[i]

	############## Write to output file #####################################

	output_file = open("output.txt", "w")

	if int(value_d) == 1:
		for j in range(1, total_var + 1):
			output_file.write(str(j) + ',' + str(h[j]) + '\n')
	else:
		#sort dictionary by values
		sorted_h = sorted(h.items(), key=operator.itemgetter(1), reverse=True)
		for j in sorted_h:
			output_file.write(str(j[0]) + ',' + str(j[1]) + '\n')

	output_file.close()
	
#Start
if __name__ == '__main__':
	main()
