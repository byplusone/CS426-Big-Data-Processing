# coding=utf-8

import numpy as np
import math
from csv import *
import matplotlib.pyplot as plt 
import matplotlib.patches as mpatches

def predictClass(weight, x):
	#print np.mat(x)
	#print np.transpose(weight)
	y =  np.mat(x) * weight
	return y[0]

def sign(y):
	if y>=0:
		return 1
	else:
		return -1

def train(dataset, learning_rate):
	y = 0
	given_label = dataset[:,3]
	weight = np.zeros((3,1)) # one constant + two features
	for i, x in enumerate(dataset):
		y = predictClass(weight,x[0:3])
		if sign(y) == given_label[i]:
			continue
		else:
			weight = weight + learning_rate * given_label[i] * np.transpose(np.mat(x[0:3]))
	return weight

def test(testset, weight):
	total = len(testset)
	good = 0.0
	given_label = testset[:,3]
	for i, x in enumerate(testset[:,0:3]):
		y = predictClass(weight, x)
		if sign(y) == given_label[i]:
			good += 1
	return good/total


if __name__ == '__main__':
	trainning_data = np.loadtxt(open("hw5train2.csv","rb"),delimiter=",",skiprows=1)
	learning_rate = 0.7
	weight = train(trainning_data, learning_rate)
	print 'Successfully trained!'
	print weight
	test_data = np.loadtxt(open("hw5test.csv","rb"),delimiter=",",skiprows=1)
	test_ratio = test(test_data, weight)
	print test_ratio


	x = [0 for i in range(1000)]
	y = [0 for i in range(1000)]
	for i in range (1000):
		x[i] = i/100
		y[i] = -float((weight[1]/weight[2]))*x[i] - float(weight[0]/weight[2])

	red_patch = mpatches.Patch(color='red', label='Positive')
	blue_patch= mpatches.Patch(color='blue',label='Negative')
	yellow_patch= mpatches.Patch(color='yellow',label='Dividing line')

	#plt.legend(loc='upper left',handles=[red_patch,blue_patch])

	for i, point in enumerate(test_data):
            if point[3] == 1:
                plt.plot(point[1],point[2],'or', color = 'r')
            else:
                plt.plot(point[1],point[2],'*', color = 'b')
	plot3 = plt.plot(x,y,color="yellow",linewidth=2)
	#plt.ylim(0.5, 5)
	#plt.xlim(4.2, 6.5)
	plt.xlabel('feature1')
	plt.ylabel('feature2')
	plt.title('Classification result')
	plt.legend(loc='upper left',handles=[red_patch,blue_patch,yellow_patch])

	plt.show()    

	# w0+w1*x1+w2*x2 = 0
	# x2 = -w1/w2







