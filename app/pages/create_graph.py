import streamlit as st
import streamlit.components.v1 as components

from app.graph import GraphBuilder
from app.utils import resolve_address, date_ok


st.header('Render A Graph')

source = st.text_input("Enter the source address").lower()
network = st.selectbox("Select the network", ["sepolia", "mainnet"])

st.write("Increasing the maximum depth increase rendering time exponentially.")
max_depth = st.slider("Select the maximum depth", 1, 10, 5)

st.write("Narrowing the search may save significant time.")
eth_threashold = st.number_input("Ignore TX under x ETH", 0.0)

datestart = st.date_input("Start date")
dateend = st.date_input("End date")


if date_res := date_ok(datestart, dateend):
    if date_res == 1:
        st.warning("The start date cannot be after the end date.")
    elif date_res == 2:
        st.warning("The end date cannot be after today.")
    st.stop()


if st.button("Vizualize"):
    st.write(f"""
        We are generating your graph for the address: {resolve_address(source)["alias"]}.\n
        This may take a few seconds, don't change any parameters.
    """)

    graph = GraphBuilder(
        network=network,
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
