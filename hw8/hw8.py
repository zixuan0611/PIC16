# Furuya Rei
from scipy.misc import imread
from skimage.transform import resize
import matplotlib.pyplot as plt
import numpy as np
from sklearn import svm

n_test = 0


# this function is provided by the professor
def boundaries(binarized,axis):
    # variables named assuming axis = 0; algorithm valid for axis=1
    # [1,0][axis] effectively swaps axes for summing
    rows = np.sum(binarized,axis = [1,0][axis]) > 0
    rows[1:] = np.logical_xor(rows[1:], rows[:-1])
    change = np.nonzero(rows)[0]
    ymin = change[::2]
    ymax = change[1::2]
    height = ymax-ymin
    too_small = 10  # real letters will be bigger than 10px by 10px
    ymin = ymin[height>too_small]
    ymax = ymax[height>too_small]
    return zip(ymin,ymax)


# this function is provided by the professor
def separate(img):
    orig_img = img.copy()
    pure_white = 255.
    white = np.max(img)
    black = np.min(img)
    thresh = (white+black)/2.0
    binarized = img<thresh
    row_bounds = boundaries(binarized, axis = 0)
    cropped = []
    for r1,r2 in row_bounds:
        img = binarized[r1:r2,:]
        col_bounds = boundaries(img,axis=1)
        rects = [r1,r2,col_bounds[0][0],col_bounds[0][1]]
        cropped.append(np.array(orig_img[rects[0]:rects[1],rects[2]:rects[3]]/pure_white))
    return cropped


# this is our function to produce the data and target for training and testing
# p is a parameter representing the percentage of the data for training
# p can be varied
def partition(data_array,target_array,p):
    total_n = len(target_array)
    n_train = int(total_n * p)
    global n_test
    n_test = total_n - n_train
    #print n_train
    #print n_test
    data_array = data_array.reshape((total_n, -1))
    train_data = []
    train_target = []
    test_data = []
    test_target = []
    a = int(n_train/3)
    b = int(n_train/3)
    temp = a + b
    c = n_train - temp
    for j in range(a):
        train_data.append(data_array[j])
        train_target.append(target_array[j])
    for j in range(23, 23+b):
        train_data.append(data_array[j])
        train_target.append(target_array[j])
    for j in range(46, 46+c):
        train_data.append(data_array[j])
        train_target.append(target_array[j])

    for k in range(a, 23):
        test_data.append(data_array[k])
        test_target.append(target_array[k])
    for k in range(23+b, 46):
        test_data.append(data_array[k])
        test_target.append(target_array[k])
    for k in range(46+c, 69):
        test_data.append(data_array[k])
        test_target.append(target_array[k])
    '''print np.shape(train_data)
    print np.shape(train_target)
    print np.shape(test_data)
    print np.shape(test_target)'''

    return train_data, train_target, test_data, test_target


# read the three symbols written by myself
# they are three Chinese characters, each with 23 examples
big_img1 = imread("write1.png", flatten = True) # flatten = True converts to grayscale
big_img2 = imread("write2.png", flatten = True)
big_img3 = imread("write3.png", flatten = True)

imgs1 = separate(big_img1)
imgs2 = separate(big_img2)
imgs3 = separate(big_img3)

# initialize our data arrays
a_data = np.zeros((69,10,10))
i = 0
for img in imgs1:
    img = resize(img, (10,10))
    a_data[i] = img
    i+=1

for img in imgs2:
    img = resize(img, (10,10))
    a_data[i] = img
    i+=1

for img in imgs3:
    img = resize(img, (10,10))
    a_data[i] = img
    i+=1

#print np.shape(a_data)

# initialize our target arrays
t_data = np.zeros(69)

for i in range(23):
    t_data[i] = 0
for i in range(23, 46):
    t_data[i] = 1
for i in range(46, 69):
    t_data[i] = 2
#print np.shape(t_data)

# get our training and testing data, target
# Note : we set p to be 0.8 here
rtrain_data, rtrain_target, rtest_data, rtest_target = partition(a_data, t_data, 0.8)

rtrain_data = np.array(rtrain_data)
rtrain_target = np.array(rtrain_target)
rtest_data = np.array(rtest_data)
rtest_target = np.array(rtest_target)

'''
idx = 27

img_test = rtrain_data[idx,:]
print "img_test",img_test.shape
img_test = img_test.reshape((10, 10))
# a = np.zeros(10,10)
plt.imshow(img_test, cmap='gray')
plt.show()
print "img_label", rtrain_target[idx]


img_test = rtest_data[idx,:]
print "img_test",img_test.shape
img_test = img_test.reshape((10, 10))
# a = np.zeros(10,10)
plt.imshow(img_test, cmap='gray')
plt.show()
print "img_label", rtest_target[idx]
'''

# Create a classifier: a support vector classifier
classifier = svm.SVC(gamma=0.001, C = 100)

# train the model
classifier.fit(rtrain_data, rtrain_target)

# print "train_target",train_target
# print "test_target", test_target


# test the model/predict the value
expected = rtest_target
predicted = classifier.predict(rtest_data)

# provide the summary of the result
print "Predicted:", predicted
print "Truth:", expected
#print n_test
a = sum(expected==predicted)*1.0/n_test * 100
print ("Accuracy: {0} %".format(a))
