from datetime import datetime
import os

import requests
from .utils import resolve_url, config, ptx, resolve_address, timestamp_to_block
from pyvis.network import Network

from streamlit_flow.elements import StreamlitFlowNode, StreamlitFlowEdge
from streamlit_flow.state import StreamlitFlowState
from streamlit_flow import streamlit_flow
from streamlit_flow.layouts import TreeLayout

# TODO manage addresses with web3.py to handle ENS


class GraphBuilder:
    def __init__(
        self,
        network="sepolia",
        lib="pyvis",
        max_depth=5,
        source=None,
        last=None,
        direction="send",
        datestart=None,
        dateend=None,
        eth_threashold=0.0,
    ):
        """ Create the graph according to the user input.
        """
        self.network = network
        self.url = resolve_url(self.network)
        self.lib = lib
        self.pyvis_net = Network()
        self.max_depth = max_depth
        self.source = source
        self.last = last
        self.direction = direction
        self.visited_txs = set()

        self.datestart = datestart
        self.dateend = dateend

        self.eth_threashold = eth_threashold

        # Blockchains don't know about time, only blocks
        self.blockstart = timestamp_to_block(
            int(datetime.combine(self.datestart, datetime.min.time()).timestamp()),
            self.network,
        ) if datestart else 0
        self.blockend = timestamp_to_block(
            int(datetime.combine(self.dateend, datetime.min.time()).timestamp()),
            self.network,
        ) if dateend else 99999999

    def fetch_transactions(
        self,
        address,
        api_key=config["ETHERSCAN_API"],
    ):
        """ Fetch all transactions for a specific Ethereum address using the 
            Etherscan API.
        """
        params = {
            "module": "account",
            "action": "txlist",
            "address": address,
            "startblock": self.blockstart,
            "endblock": self.blockend,
            "sort": "asc",
            "apikey": api_key
        }

        response = requests.get(self.url, params=params)
        data = response.json()

        # Check for errors in the response
        if data["status"] != "1":
            return None
        return data["result"]

    def filter_transactions(self, tx, sender, direction="send"):
        """ Filter transactions based on the direction and the source address.
            Not used by the actual algorithm, but useful for debugging.
        """
        if (direction == "receive" and tx['to'].lower() == sender.lower()) \
                or (direction == "send" and tx['from'].lower() == sender.lower()):
            return tx
        return False

    def test_fetch_transactions(self):
        """ Test the fetch_transactions method, and print the first 5 transactions.
        """
        try:
            txs = self.fetch_transactions(self.source)
            print(f"Found {len(txs)} transactions:")
            filtered_txs = [tx for tx in txs if self.filter_transactions(
                tx, self.source, self.direction)]
            print(f"Filtered {len(filtered_txs)} transactions")

            for tx in txs[:5]:
                ptx(tx, self.source)
        except Exception as e:
            print(e)

    def populate_graph(self, address, current_depth=0):
        """ Populate the graph with transactions starting from the given address.
            Recursively fetch transactions for the given address and add nodes 
            and edges to the graph. This is where the magic happens.

            Args:
                address (str): The Ethereum address to start from.
                current_depth (int): The current depth in the graph traversal.
                txs_visited (set): A set to keep track of visited transactions.

            Returns:
                None
        """
        if current_depth >= self.max_depth:
            return

        txs = self.fetch_transactions(address)

        if not txs:
            return

        for tx in txs:
            if tx["hash"] in self.visited_txs:
                continue
            if not tx["from"] or not tx["to"]:
                continue
            if not int(tx['value']) > self.eth_threashold:
                continue

            self.visited_txs.add(tx["hash"])

            receiver = tx["to"]
            if receiver != address.lower():  # Considering we are in send, TODO: Add receive
                resolved_receiver = resolve_address(receiver)
                self.add_nodes(receiver.casefold(), resolved_receiver)
                self.add_edge(
                    address.casefold(),
                    receiver.casefold(),
                    **{
                        "title": tx["hash"],
                    },
                )
                if resolved_receiver["continue"]:  # Stops if address is known
                    self.populate_graph(
                        receiver,
                        current_depth + 1,
                    )
                else:
                    continue

    def add_nodes(self, id, address, *args, **kwargs):
        """ Add a node to the graph. Ad the IDs are unique,
            a node will only be created if it doesn't already exist.
        """
        if self.lib == "pyvis":
            self.pyvis_net.add_node(
                id,
                label=address["alias"],
                title=address["address"],
                color=kwargs.get("color", None),
                borderWidth=kwargs.get("borderWidth", 1),
                borderWidthSelected=kwargs.get("borderWidthSelected", 2),
                size=kwargs.get("size", 15),
            )

    def add_edge(self, src, dest, *args, **kwargs):
        """ Add an edge to the graph. Pointing from the source to the destination.
        """
        if self.lib == "pyvis":
            self.pyvis_net.add_edge(
                src,
                dest,
                arrows=kwargs.get(
                    "arrows", {"to": {"enabled": True, "scaleFactor": 0.4}}),
                color=kwargs.get("color", None),
                **kwargs,
            )

    def build_graph(self):
        """ Create the source node, the calls the recursive method that
            builds the transaction graph for the given source address.
        """
        self.add_nodes(
            self.source.casefold(),
            resolve_address(self.source),
            **{"color": {"background": "red", "border": "black"}},
        )
        self.populate_graph(self.source, current_depth=0)

    def show_graph(self):
        """ Save the graph in the system.
        """
        if self.lib == "pyvis":
            # Get or create folder
            filepath = "./pyvis_output/{}/".format(
                resolve_address(self.source)["alias"],
            )
            filename = "{}_depth_{}.html".format(
                datetime.now().strftime("%Y%m%d_%H%M%S"),
                self.max_depth,
            )
            try:
                os.makedirs(filepath)
            except FileExistsError:
                pass

            self.pyvis_net.write_html(
                filepath + filename,
                open_browser=False,
            )
            return filepath + filename

        return None

    def clear_graph(self):
        """ Clear the graph nodes and edges.
        """
        self.pyvis_net = Network(directed=True)
        self.visited_txs = set()
