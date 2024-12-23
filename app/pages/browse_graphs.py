import os

import streamlit as st
import streamlit.components.v1 as components


def file_selector(folder_path='./pyvis_output/'):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select a file', filenames)
    return os.path.join(folder_path, selected_filename)


filename = file_selector()
filename = file_selector(filename)

with open(filename, "r") as HtmlFile:
    source_code = HtmlFile.read()
    components.html(source_code, height=620, scrolling=True)
