import streamlit as st
from app.utils import db, fetch_address, resolve_address

address = st.text_input("Enter the address").lower()


if len(address) != 42 or not address.startswith("0x"):
    st.warning("Please enter a valid address")
    st.stop()

db_address = fetch_address(address)

if db_address:
    st.warning("This address is already known")
    st.write(f"Alias: {resolve_address(address)['alias']}")
    st.stop()

else:
    alias = st.text_input("Enter the alias")
    if alias:
        type_ = st.selectbox(
            "Select the type",
            ["smart contract", "account", "token", "exchange", "unknown"],
        )
        if type_:
            malicious = st.checkbox("Is this address malicious?")
            st.write(
                "A deadend address stops the graph traversal at this address.")
            continue_ = st.checkbox("Continue traversal after this address?")

        submit = st.button("Submit")
        if submit:
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
