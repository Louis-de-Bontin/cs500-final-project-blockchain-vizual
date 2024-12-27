import os

import streamlit as st
import streamlit.components.v1 as components


st.header('Browse Graphs')


def file_selector(label, folder_path="./pyvis_output/"):
    """ For a given path, returns a Streamlit element to list
        the files and folder in the path.
    """
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox(
        label,
        filenames,
        placeholder="Select the type",
        index=None,
    )
    if selected_filename:
        return os.path.join(folder_path, selected_filename)


# Generates a 2 level menu that allows the user to select a folder and then a file
# When clicking on the file, it will display the graph in the browser
foldername = file_selector("Select An Address")
if foldername:
    filename = file_selector("Select A Graph", foldername)

    if filename:
        with open(filename, "r") as HtmlFile:
            source_code = HtmlFile.read()
            components.html(source_code, height=620, scrolling=True)
