import random
from typing import Any, List, Tuple

import numpy as np
import pandas as pd
import streamlit as st
import logging
from sklearn.model_selection import train_test_split


def data_prep(df: pd.DataFrame, pos) -> Tuple[List, List, List, List]:
    """
    Purpose:
        Prep data for modeling
    Args:
        df - Pandas dataframe
    Returns:
        test_features - test set features
        train_features - train set feautres
        test_target -  test set target
        train_target - train set target
    """
    # Specify the target classes
    target_string = pos.selectbox("Select Target Column", df.columns)
    target = np.array(df[target_string])

    # Select Features you want
    feature_cols = pos.multiselect("Select Modeling Features", df.columns)

    # Get all features
    features = df[feature_cols]
    featurestmp = np.array(features)
    feats = []
    # find all bad rows
    for index, featarr in enumerate(featurestmp):
        try:
            featarr = featarr.astype(float)
            feats.append(featarr)
        except Exception as error:

            pos.error(error)
            pos.error(featarr)
            pos.stop()

    featuresarr = np.array(feats)

    # Split Data
    randInt = random.randint(1, 200)

    (
        test_features,
        train_features,
        test_target,
        train_target,
    ) = train_test_split(featuresarr, target, test_size=0.75, random_state=randInt)

    return (
        test_features,
        train_features,
        test_target,
        train_target,
    )
