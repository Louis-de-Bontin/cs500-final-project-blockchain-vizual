from dotenv import dotenv_values
import csv
from cs50 import SQL

import requests
from datetime import datetime

config = dotenv_values(".env")
db = SQL("sqlite:///addresses_list/addresses.db")


def resolve_url(network) -> str:
    """ Resolve the Etherscan API URL based on the network.
    """
    if network.lower() == "mainnet" or network.lower() == "ethereum":
        return "https://api.etherscan.io/api"
    if network.lower() == "sepolia":
        return "https://api-sepolia.etherscan.io/api"
    else:
        raise Exception(f"{network} not supported")


def ptx(tx, address=None):
    """ Print a transaction with a somewhat human readable format.
    """
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
    """ Shrink a hexadecimal address to make it more readable.
    """
    return f"{hexa[:4]}...{hexa[-3:]}"


def fetch_address(address):
    """ Fetch an address from the database.
    """
    return db.execute(
        """
            SELECT address, alias, malicious, type, continue 
            FROM addresses WHERE LOWER(address) = LOWER(?) LIMIT 1;
        """,
        address,
    )


def resolve_address(address):
    """ Resolve an address to its alias if it's known, otherwise shrink it.
    """
    if db_address := fetch_address(address):
        return db_address[0]
    return {
        "address": address,
        "alias": shrink_hexa(address),
        "continue": True,
    }


def timestamp_to_block(timestamp, network="sepolia"):
    """ Convert a timestamp to a block number.
    """
    url = resolve_url(network)
    params = {
        "module": "block",
        "action": "getblocknobytime",
        "timestamp": timestamp,
        "closest": "before",
        "apikey": config["ETHERSCAN_API"],
    }
    response = requests.get(url, params=params).json()
    if response["message"] != "OK":
        raise Exception(f"Error: {response['message']}")
    return int(response["result"])


def date_ok(datestart, dateend) -> int:
    """ Return 1 if the start date is after the end date.
        Return 2 if enddate is after today.
        Return 0 otherwise.
    """
    if datestart and dateend:
        if datestart > dateend:
            return 1
    if dateend and dateend > datetime.now().date():
        return 2
    return 0
