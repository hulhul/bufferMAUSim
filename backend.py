import joblib
from sklearn.linear_model import LinearRegression
from sdv.single_table import CTGANSynthesizer
from sdv.metadata import SingleTableMetadata
import pandas as pd
import numpy as np


#to load the model
def load_model() -> LinearRegression:
    with open("lr_model.pkl", 'rb') as file:
        data = joblib.load(file)
    
    return data
    


def prediction(model: LinearRegression, synthData: CTGANSynthesizer, params: dict = None, sample_size:int = 200):
    newData = synthData.sample(sample_size)
    if params is not None:
        for x in params:
            newData[x] = params[x]
    print(newData)
    
    result = model.predict(newData)
    return np.mean(result), np.std(result)

def load_synthetic() -> CTGANSynthesizer:
    return CTGANSynthesizer.load(filepath='synthetic.pkl')



