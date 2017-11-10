# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 14:39:37 2017

@author: mducoffe

datasets preprocessing
"""

import numpy as np
import keras.utils.np_utils as kutils
from keras.datasets import mnist, cifar10
import scipy.misc as misc
import keras.backend as K
import os

SVHN_PATH='./svhn'

def build_mnist(num_sample):
    
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    if K.image_dim_ordering() == "th":
        x_train = x_train.reshape(x_train.shape[0], 1, 28, 28)
        x_test = x_test.reshape(x_test.shape[0], 1, 28, 28)
        #input_shape = (1, img_rows, img_cols)
    else:
        x_train = x_train.reshape(x_train.shape[0], 28, 28, 1)
        x_test = x_test.reshape(x_test.shape[0], 28, 28, 1)
        
        # we force the data to be channel first
        x_train = x_train.transpose((0,3,1,2))
        x_test = x_test.transpose((0,3,1,2))
    """
    # for VGG we need to resize the data
    if img_rows!=28 or img_cols!=28:
        # we need to resize the image (apply bilinear interpolation)
        x_train_ = [ misc.imresize(x_train[i,0,:,:], (img_rows, img_cols))[None,:,:] for i in range(x_train.shape[0])]
        x_test_ = [ misc.imresize(x_test[i,0,:,:], (img_rows, img_cols))[None,:,:] for i in range(x_test.shape[0])]
        x_train = np.array(x_train_)
        x_test = np.array(x_test_)
    """
    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')
    x_train /= 255
    x_test /= 255
    
    N = len(x_train)
    index = np.random.permutation(N)
    x_train = x_train[index]
    y_train = kutils.to_categorical(y_train[index])
    
    x_L = x_train[:num_sample]; y_L = y_train[:num_sample]
    
    x_U = x_train[num_sample:]; y_U = y_train[num_sample:]
    
    return (x_L, y_L), (x_U, y_U), (x_test, kutils.to_categorical(y_test))
    
    
def build_svhn(num_sample):
    import scipy.io as io
    
    dico_train = io.loadmat(os.path.join(SVHN_PATH,'train_32x32.mat'))
    x_train = dico_train['X']
    x_train = x_train.transpose((3, 0,1, 2))
    y_train = dico_train['y'] -1
    
    dico_test = io.loadmat(os.path.join(SVHN_PATH,'test_32x32.mat'))
    x_test = dico_test['X']
    x_test = x_test.transpose((3,0,1, 2))
    y_test = dico_test['y'] -1

    
    x_train = x_train.astype('float32')
    x_train /= 255.0
    x_test = x_test.astype('float32')
    x_test /= 255.0
    
    x_train = x_train.transpose((0,3,1,2))
    x_test = x_test.transpose((0,3,1,2))
    """
    def resize(img, img_rows, img_cols):
        new_img = np.zeros((3,img_rows, img_cols))
        new_img[0] = misc.imresize(img[0], (img_rows, img_cols))
        new_img[1] = misc.imresize(img[1], (img_rows, img_cols))
        new_img[2] = misc.imresize(img[2], (img_rows, img_cols))
        
        return new_img
    """
    if img_rows!=32 or img_cols!=32:
        # we need to resize the image (apply bilinear interpolation)
        x_train_ = [ resize(x_train[i], img_rows, img_cols) for i in range(x_train.shape[0])]
        x_test_ = [ resize(x_train[i], img_rows, img_cols) for i in range(x_test.shape[0])]
        x_train = np.array(x_train_)
        x_test = np.array(x_test_)
    
    y_train = kutils.to_categorical(y_train)
    y_test = kutils.to_categorical(y_test)
    N = len(x_train)
    index = np.random.permutation(N)
    x_train = x_train[index]
    y_train = y_train[index]
    
    x_L = x_train[:num_sample]; y_L = y_train[:num_sample]
    x_U = x_train[num_sample:]; y_U = y_train[num_sample:]
    
    return (x_L, y_L), (x_U, y_U), (x_test, y_test)

    
def build_cifar(num_sample):
    (x_train, y_train), (x_test, y_test) = cifar10.load_data()
    
    def resize(img, img_rows, img_cols):
        new_img = np.zeros((3,img_rows, img_cols))
        new_img[0] = misc.imresize(img[0], (img_rows, img_cols))
        new_img[1] = misc.imresize(img[1], (img_rows, img_cols))
        new_img[2] = misc.imresize(img[2], (img_rows, img_cols))
        
        return new_img
    """
    if img_rows!=32 or img_cols!=32:
        # we need to resize the image (apply bilinear interpolation)
        x_train_ = [ resize(x_train[i], img_rows, img_cols) for i in range(x_train.shape[0])]
        x_test_ = [ resize(x_train[i], img_rows, img_cols) for i in range(x_test.shape[0])]
        x_train = np.array(x_train_)
        x_test = np.array(x_test_)
    """
    x_train = x_train.astype('float32')
    x_train /= 255.0
    x_test = x_test.astype('float32')
    x_test /= 255.0
    
    y_train = kutils.to_categorical(y_train)
    y_test = kutils.to_categorical(y_test)
    N = len(x_train)
    index = np.random.permutation(N)
    x_train = x_train[index]
    y_train = y_train[index]
    
    x_L = x_train[:num_sample]; y_L = y_train[:num_sample]
    x_U = x_train[num_sample:]; y_U = y_train[num_sample:]
    
    
    return (x_L, y_L), (x_U, y_U), (x_test, y_test)

def build_data_func(dataset_name, num_sample):
    dataset_name = dataset_name.lower()
    
    assert (dataset_name in ['mnist', 'svhn', 'cifar']), 'unknown dataset {}'.format(dataset_name)
    labelled = None; unlabelled=None; test=None;
    if dataset_name=='mnist':
        labelled, unlabelled, test = build_mnist(num_sample)
    
    if dataset_name=='svhn':
        # TO DO
        labelled, unlabelled, test = build_svhn(num_sample)
    
    if dataset_name=='cifar':
        # TO DO
        labelled, unlabelled, test = build_cifar(num_sample)
        
    return labelled, unlabelled, test
    
def getSize(dataset_name):
    dataset_name = dataset_name.lower()
    assert (dataset_name in ['mnist', 'svhn', 'cifar']), 'unknown dataset {}'.format(dataset_name)
    
    if dataset_name=='mnist':
        return (1,28,28)
    
    if dataset_name=='svhn':
        return (1,32,32)
    
    if dataset_name=='cifar':
        return (1,32,32)
        
    return None
