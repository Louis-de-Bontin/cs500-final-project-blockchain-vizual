import csv
import json
from cs50 import SQL
import os


dir = os.path.dirname(os.path.abspath(__file__))

db = SQL(f"sqlite:///addresses_list/addresses.db")


def kaggle_dataset_to_csv(input, output):
    """ Format the csv downloaded from Kaggle into a csv file with the following columns:

            address, alias, type, malicious, continue

        See README.md to see the source.
    """
    with open(input) as f:
        # Read the csv file into a dict
        rows = csv.DictReader(f)
        existing_addresses = set()
        try:
            with open(output, "r") as f2:
                reader = csv.reader(f2)
                existing_addresses = {row[0] for row in reader}
        except FileNotFoundError:
            pass

        with open(output, "a") as f2:
            writer = csv.writer(f2)

            for row in rows:
                if row["Address"].lower() in existing_addresses:
                    continue
                if not row["Name"]:
                    continue
                address = row["Address"].lower()
                alias = row["Name"]
                type = row["Contract Type"] if row["Contract Type"] else row["Account Type"]
                malicious = True if row["Label"] != "Legit" else False
                writer.writerow(
                    [address.lower(), alias, type, malicious, False])


def ethereum_list_repo_to_csv_malicious(input, output, malicious=True):
    """ Format the json files from the ethereum-lists repo into a csv file with 
        the following columns:

            address, alias, type, malicious.

        See README.md to see the source.
    """
    with open(input) as f:
        addresses = json.load(f)

        existing_addresses = set()
        try:
            with open(output, "r") as f2:
                reader = csv.reader(f2)
                existing_addresses = {row[0] for row in reader}
        except FileNotFoundError:
            pass

        with open(output, "a") as f2:
            writer = csv.writer(f2)
            for address in addresses:
                if address["address"] in existing_addresses:
                    continue
                if not address["comment"]:
                    continue

                alias = address["comment"]
                address_type = "account"
                writer.writerow(
                    [address["address"].lower(), alias, address_type, malicious, False])


def ethereum_list_repo_to_csv_not_malicious(output):
    source = "./ethereum-lists-master/src/"
    folders = ["contracts", "tokens"]

    for folder in folders:
        child_folder = f"{source}{folder}/eth/"

        for file in os.listdir(child_folder):
            with open(f"{child_folder}{file}") as f:
                existing_addresses = set()
                try:
                    with open(output, "r") as f2:
                        reader = csv.reader(f2)
                        existing_addresses = {row[0] for row in reader}
                except FileNotFoundError:
                    pass

                address = json.load(f)
                if address["address"] in existing_addresses:
                    continue

                # Write new addresses to the CSV file
                with open(output, "a") as f2:
                    writer = csv.writer(f2)

                    alias = address["name"]
                    address_type = folder[:-1]
                    writer.writerow(
                        [address["address"].lower(), alias, address_type, False, False])


def csv_to_db(file=dir + "/addresses_formated.csv"):
    """ Read the csv file and insert the data into the database.
        Makes sure there are no duplicates.
    """
    with open(file, "r") as f:
        rows = csv.DictReader(f)
        i = 0
        for row in rows:
            try:
                res = db.execute(
                    """
                        INSERT INTO addresses (address, alias, type, malicious, continue) 
                        VALUES (?, ?, ?, ?, ?);
                    """,
                    row["address"].lower(),
                    row["alias"],
                    row["type"],
                    True if row["malicious"] == "True" else False,
                    True if row["continue"] == "True" else False,
                )
            except ValueError:
                # Duplicate...
                pass
            if i % 1000 == 0:
                print(f"Loaded {i} addresses...")
            i += 1


def all_to_csv():
    """ Format all the data into a single csv file.
    """
    output_csv = dir + "/addresses_formated_copy.csv"
    kaggle_dataset_to_csv(dir + "/addresses.csv", output_csv)
    ethereum_list_repo_to_csv_malicious(
        dir + "/ethereum-lists-master/src/addresses/addresses-darklist.json",
        output_csv,
    )
    ethereum_list_repo_to_csv_not_malicious(output_csv)
