# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 21:26:53 2017

@author: Norvell
"""

import numpy as np
import tensorflow as tf
import pandas as pd
import random
import houseDB
import _pickle as cPickle
from numpy import argmax
from keras.models import Sequential, load_model
from keras.layers import Dense, Activation
from keras.utils import np_utils
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import confusion_matrix
#from sklearn.model_selection import RepeatedKFold


database = houseDB.HouseDB()

class NeuralNet():
    numrows = 0
    diag = [None]
    pid = [None]
    def __init__(self):
        #self.model_filename = 'HOUSE_model.h5'
        #self.clf_filename = 'HOUSE_clf.save'
        self.train_neural_network()
        print("NN loaded")
        
    def train_neural_network(self):
        #print('training')
        global Y
        global encoder
        seed = 2
        
        # fix random seed for reproducibility
        np.random.seed(seed)
        
        
        # load dataset
        dataframe = np.asarray(database.readDB(), dtype='float16')
        self.X = dataframe[:,1:90]
        self.Y = dataframe[:,90]
        
        numrows = self.X.shape[0]
        NeuralNet.numrows = self.X.shape[0]
        numcols = self.X.shape[1]
        
        # encode class values as integers
        self.encoder = LabelEncoder()
        integer_encoded = self.encoder.fit_transform(self.Y)
        self.clf = MLPClassifier(solver='lbfgs', hidden_layer_sizes=(30,), random_state=1, warm_start=True)

        # convert integers to dummy variables (i.e. one hot encoded)
        dummy_y = np_utils.to_categorical(integer_encoded)
        onehot_encoder = OneHotEncoder(sparse=False)
        integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
        onehot_encoded = onehot_encoder.fit_transform(integer_encoded)
        total_acc = []
        
        # create model
        model = Sequential()
        model.add(Dense(2, batch_size=numrows, input_dim=numcols, kernel_initializer='normal', activation='relu'))
        model.add(Dense(4, kernel_initializer='normal', activation='sigmoid'))
        
        # Compile model
        model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
        
        X_train, X_test, Y_train, Y_test = train_test_split(self.X, dummy_y, test_size=0.0, random_state=seed)
        
        # fit the model
        model.fit(X_train, Y_train, validation_data=(X_train, Y_train), epochs=200, batch_size=numrows, verbose=0)
        self.clf.fit(X_train, Y_train)
        
        return "Neural Network Trained"

# =============================================================================
#         rkf = RepeatedKFold(n_splits=2, n_repeats=2, random_state=seed)
#         for X_test, Y_test in rkf.split(X):
#             print("%s %s" % (clf.score(X_test, Y_test)))
# =============================================================================

        #model.save(self.model_filename)
        
        #s = open(self.clf_filename, 'wb')
        #cPickle.dump(clf, s)
        #s.close()
 
        #print('trained')
    
    def predict_neural_network(self, varlist):
        global encoder
        global Y
        vararray = np.array(varlist, dtype='float64')
        patient_test = vararray     

        #l = open(self.clf_filename, 'rb')
        #clf = cPickle.load(l)
        #l.close()
        
        # Loading the saved decision tree model pickle
        #model = load_model(self.model_filename)
        
        self.encoder.fit(self.Y)
        a = np.reshape(patient_test, (1, -1))
        prediction = self.clf.predict(a)
        inverted = self.encoder.inverse_transform([argmax(prediction)])
        acc = self.clf.predict_proba(a) *100
        if(inverted == 0):
            diagnosis = 'Unknown condition'
        if(inverted == 1):
            diagnosis = 'Kidney Disease'
        if(inverted == 2):
            diagnosis = 'Herniated Disc'
        if(inverted == 3):
            diagnosis = 'Brain Tumor'
        string = 'Diagnosis: {:.2f}% chance you have {}'.format(acc[0,int(inverted)],diagnosis)
        print('Diagnosis: {}% chance you have {}'.format(acc[0,int(inverted)],diagnosis))
        if(acc[0,int(inverted)] < 50):
            string = "Diagnosis: Neural Net confidence below 50%; No condition recognized"
            inverted[0] = 0
        varlist.append(str(int(inverted[0])))
        tempnum = str(NeuralNet.numrows+1)
        NeuralNet.pid[0] = tempnum
        NeuralNet.diag[0] = str(int(inverted[0]))
        print(NeuralNet.pid)
        print(NeuralNet.diag)
        return string
    
    def test_neural_network(self):
        global encoder
        global Y
        dataframe = np.asarray(database.readDB(), dtype='float16')
        testX = dataframe[:,1:90]
        testY = dataframe[:,90] 
        patient_test = testX
        predY = []
        #l = open(self.clf_filename, 'rb')
        #clf = cPickle.load(l)
        #l.close()
        
        # Loading the saved decision tree model pickle
        #model = load_model(self.model_filename)
        length= len(testX)
        self.encoder.fit(self.Y)
        for i in range(0,length):
            a = np.reshape(testX[i], (1, -1))
            prediction = self.clf.predict(a)
            inverted = self.encoder.inverse_transform([argmax(prediction)])
            acc = self.clf.predict_proba(a) * 100
            if(inverted == 0):
                diagnosis = 'Unknown condition'
            if(inverted == 1):
                diagnosis = 'Kidney Disease'
            if(inverted == 2):
                diagnosis = 'Herniated Disc'
            if(inverted == 3):
                diagnosis = 'Brain Tumor'
            predY.append(int(inverted[0]))
            print(acc)
            print('Diagnosis: {}% chance you have {}'.format(acc[0,int(inverted)],diagnosis))
        accuracy = confusion_matrix(predY, testY)
        accuracypercentage = np.array(accuracy.sum(0), dtype="float")
        accuracypercentage[0] = float(accuracy[0][0])/float(accuracypercentage[0])
        accuracypercentage[1] = float(accuracy[1][1])/float(accuracypercentage[1])
        accuracypercentage[2] = float(accuracy[2][2])/float(accuracypercentage[2])
        accuracypercentage[3] = float(accuracy[3][3])/float(accuracypercentage[3])
        print(accuracypercentage)
        print(accuracy)
        
        return accuracypercentage, accuracy
        
if __name__ == "__main__":
    
    app = NeuralNet()
    app.train_neural_network()
    app.test_neural_network()
