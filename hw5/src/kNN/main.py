import csv
from numpy import *
from matplotlib import *
from methods import *
# coding=utf-8

k=5;
# k=raw_input("Enter the number k:")
# k=int(k)

# read training data and test data from .csv file
train_matrix=loadtxt(open('hw5train.csv','rb'),delimiter=',',skiprows=1)
test_matrix=loadtxt(open('hw5test.csv','rb'),delimiter=',',skiprows=1)
train_data=train_matrix[:,0:2]
train_label=train_matrix[:,2]
test_data=test_matrix[:,0:2]
test_label=test_matrix[:,2]
assign_label=[0 for i in range(len(test_label))]

train_size=len(train_data)
test_size=len(test_data)

# pick k nearest neighbours for each test sample
knn=[[] for i in range(test_size)]
for i in range(test_size):
    knn[i]=[0 for j in range(k)]
    knn[i]=calculateknn(test_data[i],train_data,k)
    assign_label[i]=generateLabel(knn[i],train_label)

# evaluation
true_positive=0
true_negative=0
false_positive=0
false_negative=0
for i in range(test_size):
    if assign_label[i]==test_label[i]==1:
        true_positive+=1
    elif assign_label[i]==test_label[i]==-1:
        true_negative+=1
    elif assign_label[i]==1 and test_label[i]==-1:
        false_positive+=1
    else:
        false_negative+=1

# visualization
drawPlot(test_data,test_label,assign_label)




