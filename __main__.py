import streamlit as st
from app.graph import GraphBuilder
from streamlit_flow import streamlit_flow
from streamlit_flow.state import StreamlitFlowState
from streamlit_flow.layouts import TreeLayout
from app import utils


graph = GraphBuilder()

st.title("EVM Vizualize : Ethereum Transaction Graph")

graph.network = st.selectbox("Select the network", ["sepolia", "mainnet"])
graph.url = utils.resolve_url(graph.network)
graph.max_depth = st.slider("Select the maximum depth", 1, 10, 5)
graph.source = st.text_input("Enter the source address").lower()

if graph.source:
    graph.build_graph()

    state = StreamlitFlowState(graph.nodes, graph.edges)

    streamlit_flow('tree_layout', state, layout=TreeLayout(
        direction='right'), fit_view=True)
