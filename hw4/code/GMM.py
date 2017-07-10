# ecoding=utf-8

import math
import numpy as np
import random

def computeProb(k, average, Sigma, my_matrix):
	m = len(my_matrix)
	prob = [[0 for i in range(k)] for j in range(m)] # prob[m][k]
	for i in range(m):
		for j in range(k):
			temp_mat = np.mat(my_matrix[i][0:3]-average[j])
			power_part = temp_mat * np.linalg.inv(np.mat(Sigma[j])) * np.transpose(temp_mat)
			power_part *= (-1/2)
			temp =15.749609945722417
			const_part = (1/temp * math.sqrt(np.linalg.det(np.mat(Sigma[j]))))
			prob[i][j] = const_part * math.exp(power_part[0,0])
	return prob

def postProb(k, my_matrix, alpha, prob):
	m = len(my_matrix)
	post = [[0 for i in range(k)] for j in range(m)] # post[m][k]
	temp = [0 for i in range(m)]

	for i in range(m):
		for j in range(k):
			temp[i] += alpha[j] * prob[i][j]

	for i in range(k):
		for j in range(m):
			post[j][i] = alpha[i] * prob[j][i] / temp[j]
	return post

def computeAvg(k, post_prob, my_matrix):
	average = np.zeros((k,3))
	m = len(my_matrix)

	for i in range(k):
		temp = 0
		for j in range(m):
			temp += post_prob[j][i]
			average[i] += np.multiply(post_prob[j][i], my_matrix[j][0:3])
		average[i] = (1/temp * average[i])
	return average

def computeSig(k, post_prob, my_matrix, average):
	Sigma = np.zeros((k,3,3))
	m = len(my_matrix)

	for i in range(k):
		temp = 0
		for j in range(m):
			temp += post_prob[j][i]
			temp_mat = np.mat(my_matrix[j][0:3] - average[i])
			#print post_prob[j][i] * np.transpose(temp_mat) * temp_mat
			#print '+'
			Sigma[i] += post_prob[j][i] * np.transpose(temp_mat) * temp_mat
		Sigma[i] = np.multiply(1/temp, Sigma[i])
	return Sigma

def computeMix(k, post_prob, my_matrix):
	m = len(my_matrix)
	alpha = [0 for i in range(k)]

	for i in range(k):
		for j in range(m):
			alpha[i] += post_prob[j][i]
		alpha[i] /= m
	return alpha

def initialGMM(k, my_matrix):
	alpha = [1.0/k for i in range(k)]
	Sigma = np.zeros((k,3,3))
	average = np.zeros((k,3))

	m = len(my_matrix)

	for i in range(k):
		average[i] = my_matrix[random.randint(0, m-1)][0:3]
		Sigma[i] = [[1,0,0],[0,1,0],[0,0,1]]
	return alpha, average, Sigma

def findCentroidGMM(k, my_matrix, label):
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

def computeDistance(x,y):
	value = 0
	for i,j in enumerate(x):
		value += (x[i] - y[i])*(x[i] - y[i])
	return value

def computeAverageDist(k, my_matrix, centroids, label):
	distance = 0
	for i,point in enumerate(my_matrix):
		distance += computeDistance(centroids[label[i]], point)
	return distance



