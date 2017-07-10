# coding=utf-8

from findCentroid import *
from plot import *
import csv
from numpy import *  

MAX_ITERATION = 10
k = 3

my_matrix = loadtxt(open("data.csv","rb"),delimiter=",",skiprows=1)
given_label = my_matrix[:,3]
centroids = computeCentroid(k, given_label, my_matrix)
plot(k, my_matrix, given_label, 'given', centroids)

centroids = initialCentroids(k, my_matrix)
#print centroids
label = [0 for i in range(len(my_matrix))]

for i in range(MAX_ITERATION):
	last_centroids = centroids
	label = findCentroid(centroids, my_matrix) # seperate points into different clusters
	centroids = computeCentroid(k, label, my_matrix) # update centroids
	#plot(k, my_matrix, label, int(i), centroids)
	if computeDifference(last_centroids, centroids) <= 0.000000001:
		print'Convergen!'
		break

plot(k, my_matrix, label, 'final', centroids)
print computeAverageDist(k, my_matrix, centroids, label)