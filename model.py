# -*- coding: utf-8 -*-
"""model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1I3rbo-iCdNdlcTlN2bWW5peZHyFN3n3T
"""

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle
import pandas as pd


def split_data(df: pd.DataFrame):

    y = df['is_canceled']
    X = df[["country","deposit_type","lead_time"]]

    return X, y


def open_data(path="data/demo.csv"):
    df = pd.read_csv(path)
    return df


def preprocess_data(df: pd.DataFrame, test=True):
    df.dropna(inplace=True)

    if test:
        X_df, y_df = split_data(df)
    else:
        X_df = df

    to_encode = ['deposit_type','country']
    for col in to_encode:
        dummy = pd.get_dummies(X_df[col], prefix=col)
        X_df = pd.concat([X_df, dummy], axis=1)
        X_df.drop(col, axis=1, inplace=True)

    if test:
        return X_df, y_df
    else:
        return X_df

def save_model(model,filename):
    pickle.dump(model,open(filename,'wb'))

def fit_and_save_model(X_df, y_df):
    model = LogisticRegression()
    model.fit(X_df, y_df)

    test_prediction = model.predict(X_df)
    accuracy = accuracy_score(test_prediction, y_df)
    print(f"Model accuracy is {accuracy}")

    save_model(model,'model.pkl')

    print(f"Model was saved to {path}")

def load_model(modelfile):
    loaded_model=pickle.load(open(modelfile,'rb'))
    return loaded_model

def load_model_and_predict(df):

    model=load_model('model.pkl')

    prediction = model.predict(df)[0]
    # prediction = np.squeeze(prediction)

    prediction_proba = model.predict_proba(df)[0]
    # prediction_proba = np.squeeze(prediction_proba)

    encode_prediction_proba = {
        0: "not_canceled",
        1: "canceled"
    }

    encode_prediction = {
        'Manual': "Car type -Manual",
        'Automatic': "Car type -Automatic:"
    }

    prediction_data = {}
    for key, value in encode_prediction_proba.items():
        prediction_data.update({value: prediction_proba[key]})

    prediction_df = pd.DataFrame(prediction_data, index=[0])
    prediction = encode_prediction[prediction]

    return prediction, prediction_df


if __name__ == "__main__":
    df = open_data()
    X_df, y_df = preprocess_data(df)
    fit_and_save_model(X_df, y_df)