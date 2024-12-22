import requests
import utils
from streamlit_flow.elements import StreamlitFlowNode, StreamlitFlowEdge

# TODO manage addresses with web3.py to handle ENS
# Refactor to let the user choose the package for graph visualization


class GraphBuilder:
    def __init__(self, network="sepolia", max_depth=5, source=None, last=None, direction="send"):
        self.network = network
        self.url = utils.resolve_url(self.network)
        self.nodes = []
        self.edges = []
        self.max_depth = max_depth
        self.source = source
        self.last = last
        self.direction = direction

    def fetch_transactions(
        self,
        address,
        start_block=0,
        end_block=99999999,
        api_key=utils.config["ETHERSCAN_API"],
    ):
        """Fetch all transactions for a specific Ethereum address using the Etherscan API."""
        params = {
            "module": "account",
            "action": "txlist",
            "address": address,
            "startblock": start_block,
            "endblock": end_block,
            "sort": "asc",  # Sort by ascending order
            "apikey": api_key
        }

        response = requests.get(self.url, params=params)
        data = response.json()

        # Check for errors in the response
        if data["status"] != "1":
            raise Exception(
                f"Error: {data['message']} - {data.get('result', '')}")

        return data["result"]

    def filter_transactions(self, tx, sender, direction="send"):
        """ Filter transactions based on the direction and the source address.
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
                utils.ptx(tx, self.source)
        except Exception as e:
            print(e)

    def populate_graph(self, address, current_depth=0, txs_visited=set()):
        if current_depth >= self.max_depth:
            return

        txs = self.fetch_transactions(address)

        if not txs:
            return

        for tx in txs:
            if tx["hash"] in txs_visited:
                continue
            if not tx["from"] or not tx["to"]:
                continue
            if not int(tx['value']) > 0:
                continue
            utils.ptx(tx, address)

            txs_visited.add(tx["hash"])

            receiver = tx["to"]
            if receiver != address.lower():  # Considering we are in send, TODO: Add receive
                self.nodes.append(StreamlitFlowNode(
                    receiver,
                    (0, 0),
                    {'content': utils.resolve_address(receiver)},
                    'default',
                    'right',
                    draggable=False
                ))
                self.edges.append(StreamlitFlowEdge(
                    f"{utils.resolve_address(
                        address)}->{utils.resolve_address(receiver)}",
                    address,
                    receiver,
                    animated=False,
                ))
                self.populate_graph(
                    receiver,
                    current_depth + 1,
                )

    def build_graph(self):
        """ Build the transaction graph for the given source address.
        """
        self.nodes.append(StreamlitFlowNode(
            self.source,
            (0, 0),
            {'content': utils.resolve_address(self.source)},
            'input',
            'right',
            draggable=False
        ))
        self.populate_graph(self.source)


# Test:
# graph = GraphBuilder()
# graph.network = "sepolia"
# graph.source = "0x2461214fc9777705b962248104a58f52bf41b3db"
# graph.test_fetch_transactions()
