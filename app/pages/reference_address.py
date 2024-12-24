import streamlit as st
from app.utils import db, fetch_address, resolve_address


def reference_address():
    st.header('Reference A New Address')

    with st.form('ERC20 Address', clear_on_submit=True):
        address = st.text_input("Enter the address").lower()

        db_address = fetch_address(address)

        alias = st.text_input("Enter the alias")
        type_ = st.selectbox(
            "Select the type",
            ["smart contract", "account", "token", "exchange", "unknown"],
            placeholder="Select the type",
            index=None,
        )
        malicious = st.checkbox("Is this address malicious?")
        st.write(
            "A deadend address stops the graph traversal at this address.")
        continue_ = st.checkbox(
            "Continue traversal after this address?")

        submit = st.form_submit_button("Reference")
        if submit:
            if len(address) != 42 or not address.startswith("0x"):
                st.warning("Please enter a valid address")
                st.stop()

            if db_address:
                st.warning("This address is already known")
                st.write(f"Alias: {resolve_address(address)['alias']}")
                st.stop()

            if not alias:
                st.warning("Please enter an alias")
                st.stop()

            if not type_:
                st.warning("Please select a type")
                st.stop()

            try:
                db.execute(
                    """
                        INSERT INTO addresses (address, alias, type, malicious, continue)
                        VALUES (?, ?, ?, ?, ?);
                    """,
                    address,
                    alias,
                    type_,
                    malicious,
                    continue_,
                )
                st.success(f"Address {alias} added to the list")
            except Exception as e:
                st.error(f"Error: {e}")
                st.stop()


reference_address()
