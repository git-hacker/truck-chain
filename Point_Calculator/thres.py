# -*- coding: utf-8 -*-
"""
Created on Sun Sep  9 05:54:54 2018

@author: King
"""

import numpy
import pandas
import keras
from keras.models import Sequential
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from keras.layers import Dense
from keras.layers import Merge

seed = 42
#numpy.random.seed(seed)

dataframe = pandas.read_csv("data4thresholdCalc1.csv", header=None)
dataset = dataframe.values

ThresComInput = dataset[:,0:9].astype(float)
ThresComOutput = dataset[:,9]


encoded = LabelEncoder().fit(ThresComOutput).transform(ThresComOutput)

def ThreshLayer():
	# create model
	twinmodel = Sequential()
	twinmodel.add(Dense(100, input_dim=9, kernel_initializer='normal', activation='relu'))
	twinmodel.add(Dense(45, kernel_initializer='normal', activation='relu'))
	twinmodel.add(Dense(20, kernel_initializer='normal', activation='relu'))
	twinmodel.add(Dense(1, kernel_initializer='normal', activation='sigmoid'))
	
	
    # Compile model
	twinmodel.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
	return twinmodel

predictors = []
predictors.append(('standardize', StandardScaler()))
predictors.append(('mlp', KerasClassifier(build_fn=ThreshLayer, epochs=100, batch_size=5, verbose=0)))
pipeline = Pipeline(predictors)
kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=seed)
results = cross_val_score(pipeline, ThresComInput, encoded, cv=kfold)

print("Larger: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))

# The output of this model is compared with human annnotators results and its simply perfect. 
# Thresholding in the point systems for Truck drivers has neve been better before. 
# From calculation, a section over graph (30% boundary is chosen for our algorithm)

#Note: the data used in this model has been mocked. Do not use it for any project. 



