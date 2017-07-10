# coding=utf-8

import random
import math

def findCentroid(centroids, my_matrix):
	label = [0 for i in range(len(my_matrix))]
	for i,point in enumerate(my_matrix):
		#print point[0:3]
		#print centroids[0]
		distance = computeDistance(point[0:3], centroids[0])
		#print distance
		for j,temp_centroid in enumerate(centroids):
			#print temp_centroid
			#print '******'
			temp_distance = computeDistance(point[0:3], temp_centroid)
			if temp_distance < distance:
				label[i] = j # j <= k
				distance = temp_distance
			else:
				continue
	return label


def computeDistance(x,y):
	value = 0
	for i,j in enumerate(x):
		value += (x[i] - y[i])*(x[i] - y[i])
	return value

def computeCentroid(k, label, my_matrix):
	centroids = [[] for i in range(k)]
	for i in range(k):
		point_num = 0
		temp_x = 0
		temp_y = 0
		temp_z = 0
		for j, temp_label in enumerate(label):
			if label[j] == i:
				point_num += 1
				temp_x += my_matrix[j][0]
				temp_y += my_matrix[j][1]
				temp_z += my_matrix[j][2]
		temp_x /= point_num
		temp_y /= point_num
		temp_z /= point_num
		centroids[i].append(temp_x)
		centroids[i].append(temp_y)
		centroids[i].append(temp_z)

	return centroids

def computeDifference(x,y):
	value = 0
	for i,j in enumerate(x):
		value += computeDistance(x[i], y[i])
	error = math.sqrt(value)
	print error
	return error

def initialCentroids(k, my_matrix):
	centroids = [[] for i in range(k)]
	total_point_num = len(my_matrix)
	for i in range(k):
		centroids[i] = my_matrix[random.randint(0, total_point_num-1)][0:3]
	return centroids