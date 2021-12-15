"""
Purpose:
    Example Streamlit app
"""

# Python imports
import logging
from typing import Type, Union, Dict, Any, List
from pathlib import Path
import json
import os
import urllib.parse

# 3rd party imports
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import streamlit as st
import seaborn as sns

# My imports
import utils
from sections.class_report import ClassReport as class_report

# TODO save files for download
def sidebar() -> None:
    """
    Purpose:
        Shows the side bar
    Args:
        N/A
    Returns:
        N/A
    """
    st.sidebar.header("Grimoire 3")

    file_name = f"apps/{st.session_state['template']['name']}_st.py"

    if os.path.exists(file_name):
        file_data = utils.read_from_file(file_name)
        dl_name = f"{st.session_state['template']['name']}_st.py"
        st.sidebar.download_button("Download Code", file_data, dl_name)


def render_section(section, pos, section_key) -> None:
    """
    Purpose:
        Shows section text
    Args:
        N/A
    Returns:
        N/A
    """

    # Basically each section type will have a speical render function
    section_name = section["name"]

    if section_name == "Classification Report":
        class_report.render_section_output(section, pos, section_key)

    if section_name == "Title":

        pos.title(section["value"])

    if section_name == "Metric":

        pos.metric(
            section["value"]["label"],
            section["value"]["value"],
            section["value"]["delta"],
        )

    if section_name == "Video":
        if section["value"]["start"]:
            pos.video(
                section["value"]["url"],
                start_time=section["value"]["start"],
            )
        else:
            pos.video(section["value"]["url"])

    if section_name == "Image":
        if section["value"]["width"]:
            pos.image(
                section["value"]["url"],
                caption=section["value"]["caption"],
                width=int(section["value"]["width"]),
            )
        else:
            pos.image(section["value"]["url"], caption=section["value"]["caption"])

    if section_name == "Markdown":

        pos.markdown(section["value"])

    if section_name == "Dataframe":

        try:
            df = pd.read_csv(section["value"])
            pos.write(df)
        except Exception as error:
            pos.error(error)

    if section_name == "Bar Chart":

        try:
            df = pd.read_csv(section["value"]["data"])
        except Exception as error:
            pos.error(error)

        # TODO add other custom options title, legend size, etc...
        chart = (
            alt.Chart(df)
            .mark_bar()
            .encode(
                x=f"{section['value']['x']}:O",
                y=section["value"]["y"],
                color=section["value"]["z"],
                tooltip=list(df.columns),
            )
            # .interactive()
            .properties(
                title="Bar Chart for "
                + section["value"]["x"]
                + ","
                + section["value"]["y"]
            )
            .configure_title(
                fontSize=20,
            )
            .configure_axis(labelFontSize=20, titleFontSize=20)
            .configure_legend(labelFontSize=20, titleFontSize=20)
        )

        pos.altair_chart(chart, use_container_width=True)

    if section_name == "Line Chart":

        try:
            df = pd.read_csv(section["value"]["data"])
        except Exception as error:
            pos.error(error)

        # TODO add other custom options title, legend size, etc...
        chart = (
            alt.Chart(df)
            .mark_line()
            .encode(
                x=f"{section['value']['x']}:O",
                y=section["value"]["y"],
                color=section["value"]["z"],
                tooltip=list(df.columns),
            )
            # .interactive()
            .properties(
                title="Bar Chart for "
                + section["value"]["x"]
                + ","
                + section["value"]["y"]
            )
            .configure_title(
                fontSize=20,
            )
            .configure_axis(labelFontSize=20, titleFontSize=20)
            .configure_legend(labelFontSize=20, titleFontSize=20)
        )

        pos.altair_chart(chart, use_container_width=True)


def app() -> None:
    """
    Purpose:
        Controls the app flow
    Args:
        N/A
    Returns:
        N/A
    """

    # get query
    query_params = st.experimental_get_query_params()

    if not "key" in query_params:
        st.error("No key provided")
        return

    # key = query_params["key"][0]
    key = query_params["key"][0]
    # print(key)
    # sidebar(key)
    # maybe key is path to file
    # Read JSON
    loaded_template = json.loads(key)

    # loaded_template = utils.load_json(key)
    # Update value
    st.session_state["template"] = loaded_template

    # st.write(st.session_state["template"])

    # Render current sections
    for index, section in enumerate(st.session_state["template"]["curr_sections"]):

        section_name = section["name"]
        section_key = f"{section_name}_{index}"

        if section_name == "Columns":

            # render cols
            num_cols = section["value"]["num_cols"]

            cols = st.columns(num_cols)
            for curr_index, col in enumerate(cols):
                try:
                    render_section(
                        section["value"]["cols"][curr_index],
                        col,
                        section_key + f"_col{curr_index}",
                    )
                except Exception as error:
                    col.error(error)

        else:
            render_section(section, st, section_key)


def main() -> None:
    """
    Purpose:
        Controls the flow of the streamlit app
    Args:
        N/A
    Returns:
        N/A
    """

    # Set Config
    st.set_page_config(
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    try:
        app()
        # sidebar()
    except Exception as error:
        st.error(error)


if __name__ == "__main__":
    main()
