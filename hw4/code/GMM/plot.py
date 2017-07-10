# coding=utf-8

from numpy import *  
import matplotlib  
import csv
import matplotlib.pyplot as plt  
from mpl_toolkits.mplot3d import Axes3D 
import time

def plot(k, my_matrix, label, num, centroids):
	fig = plt.figure()  
	ax = fig.add_subplot(111, projection='3d')  
	X = my_matrix[:,0]  
	Y = my_matrix[:,1]  
	Z = my_matrix[:,2]
	C = ['b', 'g', 'r', 'y']

	title = str(num) + 'th iteration'
	ax.set_title(title)
	for i in range(k):
		for j,temp_label in enumerate(label):
			if temp_label == i:
				ax.scatter(X[j],Y[j],Z[j],c=C[i])
	for centroid in centroids:
		#print centroids
		ax.scatter(centroid[0], centroid[1], centroid[2],s=40, c='m', norm=1, marker='*')
 
	plt.show()

def newplot(k, my_matrix, label, num):
	fig = plt.figure()  
	ax = fig.add_subplot(111, projection='3d')  
	X = my_matrix[:,0]  
	Y = my_matrix[:,1]  
	Z = my_matrix[:,2]
	C = ['b', 'g', 'r', 'y']

	title = str(num) + 'th iteration'
	ax.set_title(title)
	for i in range(k):
		for j,temp_label in enumerate(label):
			if temp_label == i:
				ax.scatter(X[j],Y[j],Z[j],c=C[i])
 
	plt.show()