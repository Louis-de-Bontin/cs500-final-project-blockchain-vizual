import streamlit as st

if __name__ == "__main__":
    print("Starting...")
    create_graph = st.Page(
        "app/pages/create_graph.py",
        title="Render Graph",
        icon=":material/help:",
    )
    browse_graph = st.Page(
        "app/pages/browse_graphs.py",
        title="Browse Graphs",
        icon=":material/bug_report:",
    )
    reference_address = st.Page(
        "app/pages/reference_address.py",
        title="Reference Address",
        icon=":material/bug_report:",
    )
    pages = [create_graph, browse_graph, reference_address]

    st.title("Vizualize Ethereum Transactions")

    page_dict = {
        "Create Graph": create_graph,
        "Browse Graph": browse_graph,
        "Reference Address": reference_address,
    }
    pg = st.navigation(pages)

    pg.run()
