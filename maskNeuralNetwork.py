# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 22:10:01 2017

@author: Norvell
"""


import keras as ka
from keras.models import Sequential
from keras.layers import *
from keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img
from keras.utils.np_utils import to_categorical
from keras import backend as K
from keras.backend import manual_variable_initialization
import numpy as np
from numpy import argmax
import cv2
import os
from sklearn.metrics import confusion_matrix

class MaskNeuralNet():
    def __init__(self):
        self.model_weights = 'HOUSE_mask_weights.h5'
        # dimensions of our images.
        self.img_width = 200
        self.img_height = 200
        
        #self.manual_variable_initialization(True)
        
    def train_neural_network(self):
        print('Training Imaging')
        
        global labels
        global input_shape
        global n_classes
        global train_generator
        global n_train_samples
        global epochs
        global validation_generator
        global n_validation_samples
        global batch_size
        
        labels = []
        
        train_data_dir = 'tumorMasks'
        validation_data_dir = 'tumorMasks' 
        epochs = 50
        batch_size = 20
        
        # this is the augmentation configuration we will use for training
        train_datagen = ImageDataGenerator(rescale=1. / 255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)
        
        # this is the augmentation configuration we will use for testing:
        # only rescaling
        test_datagen = ImageDataGenerator(rescale=1. / 255)
        
        train_generator = train_datagen.flow_from_directory(train_data_dir, target_size=(self.img_width, self.img_height),
                                                            batch_size=batch_size, class_mode='categorical')
        
        validation_generator = test_datagen.flow_from_directory(validation_data_dir, target_size=(self.img_width, self.img_height),
                                                                batch_size=batch_size, class_mode='categorical')
        
        n_train_samples = len(train_generator.filenames)
        n_validation_samples = len(validation_generator.filenames) 
        n_classes = len(train_generator.class_indices)
        labels = train_generator.class_indices
        print(n_train_samples)
        print(n_validation_samples)
        print(n_classes)
        print(labels)
        
        if K.image_data_format() == 'channels_first':
            input_shape = (3, self.img_width, self.img_height)
        else:
            input_shape = (self.img_width, self.img_height, 3)
        
        self.model = Sequential()
        self.model.add(Conv2D(32, (3, 3), input_shape=input_shape))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        
        self.model.add(Conv2D(32, (3, 3)))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        
        self.model.add(Conv2D(64, (3, 3)))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        
        self.model.add(Flatten())
        self.model.add(Dense(64))
        self.model.add(Activation('relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(n_classes))
        self.model.add(Activation('softmax'))
        
        self.model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['mse','accuracy'])
        mseError = []
        self.model.fit_generator(train_generator, steps_per_epoch=n_train_samples // batch_size, epochs=50, verbose=2,
                            validation_data=validation_generator, validation_steps=n_validation_samples // batch_size)
#==============================================================================
#         print(weights.history['mean_squared_error'])
#         minIndex = weights.history['mean_squared_error'].index(min(weights.history['mean_squared_error']))
#         print(min(weights.history['mean_squared_error']))
#         print(minIndex)
#         minIndex = weights.history['loss'].index(min(weights.history['loss']))
#         print(min(weights.history['loss']))
#         print(minIndex)
#==============================================================================
        # Prevent Keras from re-initializing all of the weights when saving
        self.model.save_weights(self.model_weights)
        print(self.model_weights)
        print('Imaging Trained')
        return "Masking Trained"

    def setup_neural_network(self):
        #print('Training Imaging')
        
        global labels
        global input_shape
        global n_classes
        global train_generator
        global n_train_samples
        global epochs
        global validation_generator
        global n_validation_samples
        global batch_size
        
        labels = []
        
        train_data_dir = 'tumorMasks'
        validation_data_dir = 'tumorMasks' 
        epochs = 50
        batch_size = 20
        
        # this is the augmentation configuration we will use for training
        train_datagen = ImageDataGenerator(rescale=1. / 255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)
        
        # this is the augmentation configuration we will use for testing:
        # only rescaling
        test_datagen = ImageDataGenerator(rescale=1. / 255)
        
        train_generator = train_datagen.flow_from_directory(train_data_dir, target_size=(self.img_width, self.img_height),
                                                            batch_size=batch_size, class_mode='categorical')
        
        validation_generator = test_datagen.flow_from_directory(validation_data_dir, target_size=(self.img_width, self.img_height),
                                                                batch_size=batch_size, class_mode='categorical')
        
        n_train_samples = len(train_generator.filenames)
        n_validation_samples = len(validation_generator.filenames) 
        n_classes = len(train_generator.class_indices)
        labels = train_generator.class_indices
        print(n_train_samples)
        print(n_validation_samples)
        print(n_classes)
        print(labels)
        
        if K.image_data_format() == 'channels_first':
            input_shape = (3, self.img_width, self.img_height)
        else:
            input_shape = (self.img_width, self.img_height, 3)
        
        self.model = Sequential()
        self.model.add(Conv2D(32, (3, 3), input_shape=input_shape))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        
        self.model.add(Conv2D(32, (3, 3)))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        
        self.model.add(Conv2D(64, (3, 3)))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        
        self.model.add(Flatten())
        self.model.add(Dense(64))
        self.model.add(Activation('relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(n_classes))
        self.model.add(Activation('softmax'))
        
        #self.model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['mse','accuracy'])
        mseError = []
        #self.model.fit_generator(train_generator, steps_per_epoch=n_train_samples // batch_size, epochs=50, verbose=2,
                            #validation_data=validation_generator, validation_steps=n_validation_samples // batch_size)
#==============================================================================
#         print(weights.history['mean_squared_error'])
#         minIndex = weights.history['mean_squared_error'].index(min(weights.history['mean_squared_error']))
#         print(min(weights.history['mean_squared_error']))
#         print(minIndex)
#         minIndex = weights.history['loss'].index(min(weights.history['loss']))
#         print(min(weights.history['loss']))
#         print(minIndex)
#==============================================================================
        # Prevent Keras from re-initializing all of the weights when saving
        #self.model.save_weights(self.model_weights)
        #print(self.model_weights)
        #print('Imaging Trained')
        return "Masking Trained"

    def predict_neural_network(self, img, mode):
        #input path
        #img = 'disctrain\Hdisc\1.jpg' #cv2.imread('HOUSE/test1/1.jpg')
        print('Predicting...')
        
        global labels
        global input_shape
        global n_classes
        global train_generator
        global n_train_samples
        global epochs
        global validation_generator
        global n_validation_samples
        global batch_size
         
        image = load_img(img, target_size=(self.img_width,self.img_height))
        width,height,channels = np.shape(image)
        print(width,height,channels)
        
        self.model = Sequential()
        self.model.add(Conv2D(32, (3, 3), input_shape=input_shape))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        
        self.model.add(Conv2D(32, (3, 3)))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        
        self.model.add(Conv2D(64, (3, 3)))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        
        self.model.add(Flatten())
        self.model.add(Dense(64))
        self.model.add(Activation('relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(n_classes))
        self.model.add(Activation('softmax'))
        if(mode==0):
            self.model.load_weights(self.model_weights)
        else:
            self.model.load_weights('HOUSE_mask_weights.h5')
        
        
        a = img_to_array(image)  
        
        # important! otherwise the predictions will be '0'  
        a = a / 255  
        
        a = np.expand_dims(a, axis=0)
        
        x = np.vstack([a])
        
        p = self.model.predict_proba(x)
        #acc = model.predict_proba(p)
        #print(p)
        classes = self.model.predict_classes(x, batch_size=batch_size)
        #print(classes)
        p = p[0,int(classes)] * 100
        
        inID = classes[0]
        
        inv_map = {v: k for k, v in labels.items()}  
        
        label = inv_map[inID] 
        
        #print(p)
        #print(label)
        print('Diagnosis: {}% chance this is a {}'.format(int(p), label))
        return(inID, int(p))
    def test_neural_network(self):
        #input path
        #img = 'disctrain\Hdisc\1.jpg' #cv2.imread('HOUSE/test1/1.jpg')
        print('Predicting...')
        
        global labels
        global input_shape
        global n_classes
        global train_generator
        global n_train_samples
        global epochs
        global validation_generator
        global n_validation_samples
        global batch_size
        
        
        train_data_dir = 'tumorMasks'
        validation_data_dir = 'tumorMasks' 
        
        train_datagen = ImageDataGenerator(rescale=1. / 255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)
        
        # this is the augmentation configuration we will use for testing:
        # only rescaling
        test_datagen = ImageDataGenerator(rescale=1. / 255)
        
        train_generator = train_datagen.flow_from_directory(train_data_dir, target_size=(self.img_width, self.img_height),
                                                            batch_size=batch_size, class_mode='categorical')
        
        validation_generator = test_datagen.flow_from_directory(validation_data_dir, target_size=(self.img_width, self.img_height),
                                                                batch_size=batch_size, class_mode='categorical')
        
        
        self.model = Sequential()
        self.model.add(Conv2D(32, (3, 3), input_shape=input_shape))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        
        self.model.add(Conv2D(32, (3, 3)))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        
        self.model.add(Conv2D(64, (3, 3)))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        
        self.model.add(Flatten())
        self.model.add(Dense(64))
        self.model.add(Activation('relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(n_classes))
        self.model.add(Activation('softmax'))
        
        self.model.load_weights(self.model_weights)
        predY = []
        trueY = []
        filenames = len(train_generator.filenames)
        for i in range(0, filenames):
            train_generator.filenames[i] = 'tumorMasks\\'+ train_generator.filenames[i]
            print(train_generator.filenames[i])
            if("Negative" in train_generator.filenames[i]):
                trueY.append(0)
            if("Positive" in train_generator.filenames[i]):
                trueY.append(1)
                
        for i in range(0, filenames):
            image = load_img(train_generator.filenames[i], target_size=(self.img_width,self.img_height))
            a = img_to_array(image)  
            
            # important! otherwise the predictions will be '0'  
            a = a / 255  
            
            a = np.expand_dims(a, axis=0)
            
            x = np.vstack([a])
            
            p = self.model.predict_proba(x)
            #acc = model.predict_proba(p)
            #print(p)
            classes = self.model.predict_classes(x, batch_size=batch_size)
            #print(classes)
            p = p[0,int(classes)] * 100
            
            inID = classes[0]
            
            inv_map = {v: k for k, v in labels.items()}  
            
            label = inv_map[inID] 
            predY.append(inID)
        accuracy = confusion_matrix(predY, trueY)
        accuracypercentage = np.array(accuracy.sum(0), dtype="float")
        accuracypercentage[0] = float(accuracy[0][0])/float(accuracypercentage[0])
        accuracypercentage[1] = float(accuracy[1][1])/float(accuracypercentage[1])
        print(accuracypercentage)
        print(accuracy)
        return accuracypercentage, accuracy
    
if __name__ == "__main__":
    
    app = MaskNeuralNet()
    app.train_neural_network()
    app.test_neural_network()