# coding=utf-8

from findCentroid import *
from plot import *
import csv
from numpy import *  
from GMM import *

MAX_ITERATION = 10
k = 3

my_matrix = loadtxt(open("data.csv","rb"),delimiter=",",skiprows=1)
given_label = my_matrix[:,3]
#plot(k, my_matrix, given_label)

#centroids = initialCentroids(k, my_matrix)
#print centroids
#label = [0 for i in range(len(my_matrix))]
'''
for i in range(MAX_ITERATION):
	last_centroids = centroids
	label = findCentroid(centroids, my_matrix) # seperate points into different clusters
	centroids = computeCentroid(k, label, my_matrix) # update centroids
	#plot(k, my_matrix, label, int(i), centroids)
	if computeDifference(last_centroids, centroids) <= 0.000000001:
		print'Convergen!'
		break
'''
average = np.zeros((k,3))
alpha = [0 for i in range(k)]
Sigma = np.zeros((k,3,3))
new_label = [0 for i in range(len(my_matrix))]


alpha, average, Sigma = initialGMM(k,my_matrix)

#print np.mat(my_matrix[10][0:3])

for temp_iter in range(MAX_ITERATION):
	# E-step
	prob = computeProb(k, average, Sigma, my_matrix)
	post_prob = postProb(k, my_matrix, alpha, prob)
	#print post_prob
	# M-step
	average = computeAvg(k, post_prob, my_matrix)
	Sigma = computeSig(k, post_prob, my_matrix, average)
	alpha = computeMix(k, post_prob, my_matrix)
	print temp_iter

	for i in range(len(my_matrix)):
		new_label[i] = argmax(post_prob[i])

centroids = findCentroidGMM(k, my_matrix, new_label)
print centroids
plot(k, my_matrix, new_label, temp_iter, centroids)
print computeAverageDist(k, my_matrix, centroids, new_label)
	#error = linalg.norm(mat(new_label) - mat(label), 2)
	#print error


