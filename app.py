# -*- coding: utf-8 -*-
"""app.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lisT9w2Ig3gOD986i_xLMANOI4ew3Pc5
"""

import pandas as pd
import streamlit as st
from PIL import Image
from model import open_data, preprocess_data, split_data, load_model_and_predict


def process_main_page():
    show_main_page()
    process_side_bar_inputs()


def show_main_page():
    image = Image.open('data/hotel.jpg')

    st.set_page_config(
        layout="wide",
        initial_sidebar_state="auto",
        page_title="Hotel Booking Cancelation",
        page_icon=image,

    )

    st.write(
        """
        # Classification.
        """
    )

    st.image(image)


def write_user_data(df):
    st.write("## your data")
    st.write(df)


def write_prediction(prediction, prediction_probas):
    st.write("## prediction")
    st.write(prediction)

    st.write("## probability of prediction")
    st.write(prediction_probas)


def process_side_bar_inputs():
    st.sidebar.header('parameters')
    user_input_df = sidebar_input_features()

    train_df = open_data()
    train_X_df, _ = split_data(train_df)
    full_X_df = pd.concat((user_input_df, train_X_df), axis=0)
    preprocessed_X_df = preprocess_data(full_X_df, test=False)

    user_X_df = preprocessed_X_df[:1]
    write_user_data(user_X_df)

    prediction, prediction_probas = load_model_and_predict(user_X_df)
    write_prediction(prediction, prediction_probas)


def sidebar_input_features():
    country = st.sidebar.selectbox("country", ('PRT', 'rare', 'GBR', 'FRA', 'ESP', 'DEU', 'IRL', 'BEL', 'USA', 'CHE'))

    deposit_type = st.sidebar.selectbox("deposit_type", ('No Deposit' 'Refundable' 'Non Refund'))

    lead_time = st.sidebar.slider("lead_time", min_value=0, max_value=709, value=200,
                            step=1)


    data = {
        "Deposit_type": deposit_type,
        "Lead_time": lead_time,
        "Country": country,
    }

    df = pd.DataFrame(data, index=[0])

    return df


if __name__ == "__main__":
    process_main_page()