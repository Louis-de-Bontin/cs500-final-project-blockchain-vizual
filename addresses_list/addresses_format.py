import csv
import json
import utils
import os


def format_csv():
    with open("./addresses_list/eth_addresses.csv") as f:
        # Read the csv file into a dict
        rows = csv.DictReader(f)
        with open("./addresses_list/formated_list.csv", "a") as f2:
            writer = csv.writer(f2)

            for row in rows:
                address = row["Address"].lower()
                alias = row["Name"] if row["Name"] else row["Tags"] if row["Tags"] else utils.shrink_hexa(
                    address)
                type = row["Contract Type"] if row["Contract Type"] else row["Account Type"]
                malicious = True if row["Label"] != "Legit" else False
                writer.writerow([address, alias, type, malicious])


def format_report(filename, malicious=True):
    # Read the json file into a list
    with open(filename) as f:
        addresses = json.load(f)

        # Read existing addresses from the CSV file
        existing_addresses = set()
        try:
            with open("./addresses_list/formated_list.csv", "r") as f2:
                reader = csv.reader(f2)
                # Assuming the address is in the first column
                existing_addresses = {row[0] for row in reader}
        except FileNotFoundError:
            # If the file doesn't exist, proceed as if it's empty
            pass

        # Write new addresses to the CSV file
        with open("./addresses_list/formated_list.csv", "a") as f2:
            writer = csv.writer(f2)
            for address in addresses:
                if address["address"] in existing_addresses:
                    continue

                alias = address["comment"] if address["comment"] else utils.shrink_hexa(
                    address["address"])
                address_type = "account"
                writer.writerow(
                    [address["address"], alias, address_type, malicious])


def format_from_folders():
    source = "./addresses_list/ethereum-lists-master/src/"
    folders = ["contracts", "tokens"]

    for folder in folders:
        child_folder = f"{source}{folder}/eth/"

        # Iterate over the files in the child folder
        for file in os.listdir(child_folder):
            with open(f"{child_folder}{file}") as f:
                # Read existing addresses from the CSV file
                existing_addresses = set()
                try:
                    with open("./addresses_list/formated_list.csv", "r") as f2:
                        reader = csv.reader(f2)
                        # Assuming the address is in the first column
                        existing_addresses = {row[0] for row in reader}
                except FileNotFoundError:
                    # If the file doesn't exist, proceed as if it's empty
                    pass

                address = json.load(f)
                if address["address"] in existing_addresses:
                    continue

                # Write new addresses to the CSV file
                with open("./addresses_list/formated_list.csv", "a") as f2:
                    writer = csv.writer(f2)

                    alias = address["name"]
                    address_type = folder[:-1]
                    writer.writerow(
                        [address["address"], alias, address_type, False])


# format_report(
#     "./addresses_list/ethereum-lists-master/src/addresses/addresses-lightlist.json",
#     False
# )
# format_from_folders()
# TODO: make it maintainable, and include a personal csv
