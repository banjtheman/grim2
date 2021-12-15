import logging
from typing import Any, Dict, List

# import streamlit as st
import pandas as pd

from .section_utils import (
    data_prep,
)
from sklearn.naive_bayes import GaussianNB
from yellowbrick.classifier import classification_report

# Not really a class, more of an interface..., nothing stateful


class ClassReport:
    def __init__(
        self,
    ):

        self.name = "Classification Report"
        self.desc = "Show Classification Report"
        self.value = ""
        self.section_json = {"name": self.name, "desc": self.desc, "value": self.value}

    def render_section_output(section, pos, section_key):

        try:
            df = pd.read_csv(section["value"])

            (
                test_features,
                train_features,
                test_target,
                train_target,
            ) = data_prep(df, pos)

            if pos.button("Train Model", key=section_key):

                pos.header("Classification Report")

                pos.markdown(
                    "The classification report visualizer displays the precision, recall, F1, and support scores for the model. In order to support easier interpretation and problem detection, the report integrates numerical scores with a color-coded heatmap. All heatmaps are in the range (0.0, 1.0) to facilitate easy comparison of classification models across different classification reports."
                )

                # Instantiate the visualizer
                visualizer = classification_report(
                    GaussianNB(),
                    train_features,
                    train_target,
                    test_features,
                    test_target,
                    support=True,
                )

                # Get the viz
                fig = visualizer.fig
                ax = visualizer.show()
                fig.axes.append(ax)

                # show the viz
                pos.write(fig)

        except Exception as error:
            pos.error(error)
