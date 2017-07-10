import random
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# pick k nearest neighbours from matrix for data, return indexes
def calculateknn(data,matrix,k):
    size=len(matrix)
    distance=[0 for i in range(size)]
    for i in range(size):
        distance[i]=calculateDistance(data,matrix[i])
        distance[i]=[i,distance[i]]
    index=[0 for i in range(k)]
    for i in range(k):
        for j in range(size-i-1):
            if distance[j][1]<distance[j+1][1]:
                distance[j],distance[j+1]=distance[j+1],distance[j]
    for i in range(k):
        index[i]=distance[size-i-1][0]
    return index

def generateLabel(indexes,label):
    positive=0
    negative=0
    for i in range(len(indexes)):
        if label[indexes[i]]==1:
            positive+=1
        else:
            negative+=1
    if positive>negative:
        return 1
    elif positive<negative:
        return -1
    else:
        rand=random.choice([-1,1])
        return rand

# calculate the distance between vector x and y
def calculateDistance(x,y):
    dim=len(x)
    value=0
    for i in range(dim):
        value+=(x[i]-y[i])*(x[i]-y[i])
    return value

def drawPlot(test_data,test_label,assign_label):
    plt.figure(1)
    red_patch = mpatches.Patch(color='red', label='Positive')
    blue_patch= mpatches.Patch(color='blue',label='Negative')
    sub1=plt.subplot(121)
    sub2=plt.subplot(122)

    plt.sca(sub1)
    plt.xlabel('x axis')
    plt.ylabel('y axis')
    plt.title('Classification with given label')
    plt.legend(loc='upper left',handles=[red_patch,blue_patch])
    plt.sca(sub2)
    plt.xlabel('x axis')
    plt.title('Classification with trained label')
    plt.legend(loc='upper left',handles=[red_patch,blue_patch])
    for i in range(len(test_data)):
        plt.sca(sub1)
        if test_label[i]==1:
            plt.plot(test_data[i][0],test_data[i][1],'ro')
        elif test_label[i]==-1:
            plt.plot(test_data[i][0], test_data[i][1], 'b*')
        plt.sca(sub2)
        if assign_label[i]==1:
            plt.plot(test_data[i][0],test_data[i][1],'ro')
        elif assign_label[i]==-1:
            plt.plot(test_data[i][0], test_data[i][1], 'b*')
    plt.show()

