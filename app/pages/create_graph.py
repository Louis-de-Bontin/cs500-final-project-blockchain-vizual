import streamlit as st
import streamlit.components.v1 as components

from app.graph import GraphBuilder
from app.utils import resolve_address


st.title("EVM Vizualize : Ethereum Transaction Graph")

network = st.selectbox("Select the network", ["sepolia", "mainnet"])
lib = st.selectbox("Select the library", ["pyvis"])
max_depth = st.slider("Select the maximum depth", 1, 10, 5)
eth_threashold = st.number_input("Ignore TX under x ETH", 0.0)
source = st.text_input("Enter the source address").lower()

datestart = st.date_input("Start date")
dateend = st.date_input("End date")

if st.button("Vizualize"):
    st.write(f"""
        We are generating your graph for the address: {resolve_address(source)["alias"]}.\n
        This may take a few seconds, don't change any parameters.
    """)

    graph = GraphBuilder(
        network=network,
        lib=lib,
        max_depth=max_depth,
        source=source,
        datestart=datestart,
        dateend=dateend,
        eth_threashold=eth_threashold,
    )

    graph.build_graph()
    st.header("Here is your graph:")
    html_path = graph.show_graph()

    graph.clear_graph()

    if html_path:
        with open(html_path, "r") as HtmlFile:
            source_code = HtmlFile.read()
            components.html(source_code, height=620, scrolling=True)
