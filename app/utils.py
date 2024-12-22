from dotenv import dotenv_values
import csv

config = dotenv_values(".env")


def load_csv(file):
    """ Load a csv with the format "address,alias,type,malicious"
        Returns a dictionary with this format:
        {
            "address": {"alias": alias, "type": type, "malicious": malicious},
            ...
        }
    """
    out = {}
    with open(file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            out[row["address"].casefold()] = {
                "alias": row["alias"],
                "type": row["type"],
                "malicious": row["malicious"],
            }
    return out


KNOWN_ADDRESSES = load_csv("addresses_list/formated_list.csv")


def resolve_url(network):
    print(f"Network: {network}")
    if network.lower() == "mainnet" or network.lower() == "ethereum":
        return "https://api.etherscan.io/api"
    if network.lower() == "sepolia":
        return "https://api-sepolia.etherscan.io/api"
    else:
        raise Exception(f"{network} not supported")


def ptx(tx, address=None):
    def direction():
        if address and tx['to'].lower() == address.lower():
            return "Received: "
        elif address and tx['from'].lower() == address.lower():
            return "Send    : "
        else:
            return "Value   : "
    print(
        "Hash: {}...{}, To: {}...{}, From: {}...{}, {}{} ETH".format(
            tx['hash'][:4],
            tx['hash'][-3:],

            tx['to'][:4],
            tx['to'][-3:],

            tx['from'][:4],
            tx['from'][-3:],

            direction(),

            int(tx['value']) / 1e18,
        )
    )


def shrink_hexa(hexa):
    return f"{hexa[:4]}...{hexa[-3:]}"


def resolve_address(address):
    if address.casefold() in KNOWN_ADDRESSES:
        return KNOWN_ADDRESSES[address.casefold()]["alias"]
    return shrink_hexa(address)
