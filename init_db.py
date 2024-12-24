from cs50 import SQL
import os
from addresses_list import addresses_format

# Database file
db_file = "addresses_list/addresses.db"

# Create connection
db = SQL(f"sqlite:///{db_file}")

# Populate the database from CSV
n_addresses = db.execute("SELECT count(*) FROM addresses;")

if n_addresses[0]["count(*)"] > 20000:
    print("Database already initialized!")
    exit()
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_file = base_dir + "/addresses_list/addresses_formated.csv"
addresses_format.csv_to_db(csv_file)

print("Database initialized successfully!")
