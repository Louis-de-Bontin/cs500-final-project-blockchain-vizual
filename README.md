# EVM Visual

### License

This project is licensed under the GNU Lesser General Public License (LGPL) v3.0.
See the [LICENSE](./LICENSE) file for details.

### Description
The idea behind this project is to be able to visualize what is happening on the blockchain. This is achieved by generating a graph where the nodes represent the addresses and the edges represent the transactions. <br>
Browsing and tracing transactions on chain explorer is a tedious and long process. With this project, it is now possible to follow transfer of value, as well as link between addresses in an easy to read visual.

This would be useful in several contexts:
- If an address has been compromised, it is possible to see where the money went. Indeed, the user would only have to input his compromised address, narrow the search to the time-frame of the hack, and see where the money went. This project includes a database of more than 27,000 known addresses linked to exchanges, hacks, scams, mixers, etc. This way, the user can see if the money went to a known address.
- Government agencies could use this tool to track money laundering, or to see if a known address is involved in a transaction.
- The user can reference known addresses himself, and can therefore use this tool to investigate an address or a transaction. This tool might be helpful to law enforcement agencies, private investigators, or even journalists.

### Why This Project?

#### Why It Fits CS50
Several concepts that I learned in CS50 are used in this project: basic graph theory, SQL and Python. The complexity is manageable while not being too simple, and the project is real-world relevant. It is a good way to apply the knowledge I acquired during the course.

#### Why It's Relevant To My Future
Needless to say that with such a project, finance and more specifically cryptos are of great interest to me. That's why I choose to work on a project linked to data science as I strive to continue studying in this field. This project is a good way to show my interest in blockchain, data science, and graph theory.

### Setup
There are 2 ways to setup this project: Docker or locally. In both cases you will need an [Etherscan API key](https://docs.etherscan.io/getting-started/viewing-api-usage-statistics).

#### Docker (Recommended)
This section assume that you have Git and Docker installed on your machine.
1. Clone the repository `git clone git@github.com:Louis-de-Bontin/cs500-final-project-blockchain-vizual.git`
2. Create a `.env` file in the root of the project and add the following line `ETHERSCAN_API = "<your-api-key>"`
3. Build the Docker image `docker build -t evm-visual .` 
4. Run the Docker container `docker run evm-visual` (the first time you run this command, the 27,000 addresses from the .csv will be loaded in the database. This process may take a few minutes)
5. Once the database is initialized and Streamlit is running, you should see the following:
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://172.17.0.2:8501
  External URL: http://42.116.164.139:8501

```
5. Open the URL labeled `Network URL` in your browser.

### How To Use
In your browser, you should see the Streamlit app. Looking at the menu on the left, you can see the following options:
###### Create Graph
This is the core of the project. This is where you can input an address, and see the hierarchy of transactions that link addresses together.
- `Enter the source address` is where you input the address you want to investigate.
- `Select the network`, select the blockchain that is relevant to your investigation. For now, only Ethereum and Sepolia (Ethereum testnet) are supported.
- `Select the maximum depth` is the maximum number of transaction that will separate your address from a last address. At some point the graph generation needs to end, otherwise the graph would never show up. Keep in mind that increasing this number may __significantly__ slow down the graph generation. If you meet addresses that have a crazy number of transactions, you can reference them in the database, see the section `Useful` for more information.
- `Ignore TX under x ETH` is an optional parameter that allows you to ignore transactions that are below a certain value. This is useful to filter out dust swaps, signatures, etc. The unit is in ETH.
- `Start date` will filter out all transactions that happened before this date. This is useful to narrow the search to a specific time-frame. This is optional. In the back-end, this is converted to a block number, as blockchain are not aware of time.
- `End date` likewise, it will filter out all transactions that happened after this date.
<br>
Once the form is completed, you can click `Visualize`, wait a bit a see the magic happen.
The source (the starting address that you input in the first line of the form) is display in red in order to differentiate it from the others.The other addresses are displayed in blue.<br>
If you hover a node or an edge, you can see the full address or transaction hash. Sadly the user can not click or copy them... An idea for future improvement.<br>
The edges are directional, and point from the sender to the receiver.<br>
__Important__: it is possible that address A sent money to address B. Then address B sent money to address A. In this case the last transaction that is met while building the graph will take on the first one. Assuming that the 2nd transaction is observed in 2nd by the graph (note that the transaction timestamp is irrelevant), this is the one that will dictate the direction of the edge. In this scenario, B will point to A in the graph. This is an other limitation that could be improved in the future.

###### Browse Graphs
Simply allows you to navigate through all the graphs you generated. Sorted by source address.

###### Reference Address
Here, you can add a new "Known Address" to the database. Check the section `Database > Structure` to understand each field. Here, you can reference address that may not be already known by the database, or that are simply relevant in your project.<br>
The user doesn't have the possibility to update or delete addresses. This is a feature that could be added in the future.

#### Local
Alternatively, you can run this project locally. 
1. Install git, python3 and pip3
2. Install sqlite3
3. Clone the repository `git clone git@github.com:Louis-de-Bontin/cs500-final-project-blockchain-vizual.git`
4. Create a `.env` file in the root of the project and add the following line `ETHERSCAN_API = "<your-api-key>"`
5. Create a virtual environment `python3 -m venv venv`
6. Activate the virtual environment `source venv/bin/activate`
7. Install the requirements `pip install -r requirements.txt`
8. Create the database `sqlite3 ./addresses_list/addresses.db < ./addresses_list/addresses_db_cmd.sql`
9. Populate the database `python3 ./init_db.py`
10. Run the app `streamlit run app.py`

### Database

#### Sources Used For Addresses
The database is an aggregation of the following sources:
- [Binance's Commitment to Transparency](https://www.binance.com/en/blog/community/our-commitment-to-transparency-2895840147147652626)
- [Etherscan](https://etherscan.io/accounts), for this source, there is no automation, as it is impossible to know if the addresses are malicious, or if the graph generation should stop when meeting one of them.
- [Ethereum List Repo](https://github.com/MyEtherWallet/ethereum-lists)
- [Kaggle Database by Hamish Hall](https://www.kaggle.com/datasets/hamishhall/labelled-ethereum-addresses)

#### Database Population Explained

I figured that it would be easier to work with a CSV. Anyone can easily load it or read it in any IDE, or even directly in the repository.
- The first difficulty was to unify all the sources in a common format. T came up with my own format that would suit the need of the project, then I created different script for different sources so that I could merge them all in a single CSV.

###### Structure
- The format of the CSV matches the format of the database. It is as follows: `address,alias,type,malicious,continue`.
- Address is the address of the account (0xblablabla).
- Alias is a human readable name for the address. It can be anything, but it is recommended to be short.
- Type is the type of the address. It can be `exchange`, `account`, `token` or `smart contract`
- Malicious is a boolean that indicates if the address is known to be malicious. An address is malicious if it is related to a scam, a hack, money laundering, etc.
- Continue is a boolean that indicates if the graph generation should stop when meeting this address. This is useful for addresses that have a crazy number of transactions, and that slow significantly the graph generation. Continuing the graph after addresses like Binance wallet makes no sens, as it is a dead-end. I also exponentially increase the number of transactions that are fetched for these addresses, bringing next to 0 value to the graph. Therefore they could be considered as dead-end. In application, that makes sens, if the money went to a mixer, it cannot be traced further. If it went to an exchange, then it is dependent on the will of the exchange to provide more information on the funds movements.

###### Population
- When executing `init_db.py`, the scripts check if the database is already significantly populated. If it isn't, it will populate it with the CSV. If it is, it will pass and not populate it again.
- Before loading the database, you can manually add addresses to the CSV. Once it is loaded, you should use the user interface to directly populate the database.

### Libraries
###### CS50
I liked the SQL implementation that comes with the CS50 library. I choose to take advantage of it.

###### Jupiter Lab
I ran some test on Jupiter Lab, and I found it very useful to test the code, and make sure the project is doable. You can find my .ipynb in the repository, though they are not very usefull. I just wrote some draft to make sure it would be doable to fetch the transactions for a given address, and build the graph.

###### Web3.py
I use it to convert timestamp to block number. In the future it would be interesting to manage the addresses with it to support ENS.

###### Requests
Quite straightforward, I use it to fetch the transactions from the Etherscan API.

###### Streamlit
The heavy and interesting work of this project is the graph generation, and its main value is in the graph visualization as well as the database. Therefore I wanted to have the easiest possible front-end to create. I'm also very allergic to CSS and JavaScript. So, for the well-being of my keyboard and my neighbors, I choose to use Streamlit.<br>
The obvious downside being that it is not possible to deploy front-end and back-end separately. This is probably something that could be enhanced in the future. But for the sake of demonstration, it is more than enough.

###### Dotenv
Manages the environment variables. It is used to store the API key for Etherscan.

###### Streamlit-flow-component
This is a third party Streamlit component that allows embedding html pages into the Streamlit interface. As Pyvis stores the graph in .html, we need this to display them.

###### Pyvis
This one took a while to pick. There are many available libraries to visualize graph. First I tried a Streamlit component, but it had 2 flows. First it didn't save the graphs, so we had no ways to browse and share existing graphs. The second one was that it was very poorly optimized and took forever to generate small graphs. So even though it was beautiful, highly customizable and interactive, I choose to pass on this one. The second one I tried was Graph Tool. Well... tried... I tried to install it, since I failed, I didn't have the opportunity to actually try the library. After wasting a few days of work trying to install Graph Tools 5 or 6 different ways, I gave up, and listed a few potential candidates. NetworkX and Graphviz seem to be popular, but they are not interactive, and ugly as sh*t, let's be honest. Graphviz seem to be the right balance between optimization and interactivness. So I choose to test it, and I was very satisfied with it.

### Graph Generation Algorithm

### Future Improvements
- Add the possibility to update and delete addresses in the database.
- Add the possibility to click on nodes and edges to be redirected on a block explorer, or copy the address or transaction hash.
- Add the possibility to ignore specific addresses during the graph generation.
- Add the possibility to ignore specific transactions during the graph generation.
- Bi-directional edges. If address A sent money to address B, and address B sent money to address A, the edge should be bi-directional.
- Create a proper UX, and make the back-end global so that users can share graph, known addresses...
- Manage addresses with web3.py to support ENS.
- Add more blockchain networks.
- Feature to see the known addresses in the front-end.
- Add the possibility to stop the graph generation if taking too long.
- Possibility to see the balance of an address from the graph.
- Can input alias instead of address, with auto-completion.
- Make the graph generation asynchronous.


#### Useful
###### Quickly see a graph
In the `Render Graph` section, fill the form as follows:
- Source address: `0x2461214FC9777705b962248104a58f52BF41B3db`
- Network: `Sepolia
- Maximum depth: `5`
- Start date: `2024-11-01`
- End date: `2024-12-26`

###### What to do if the graph generation is too slow
- Reduce the maximum depth.
- Narrow the search to a specific time-frame.
- Ignore transactions under a certain value.
- When meeting an address with a crazy number of transactions, which slows significantly the graph generation, it is recommended to reference this address, un-checking `Continue` so the the graph generation stops when meeting this address.

### Project Structure
|final_project/
├── addresses_list/
│   ├── addresses_db_cmd.sql
│   ├── addresses_format.py
│   ├── addresses_formatted.csv
│   ├── addresses.db
├── app/
│   ├── pages/
│   │   ├── browse_graphs.py
│   │   ├── create_graph.py
│   │   ├── reference_address.py
│   ├── graph.py
│   ├── utils.py
├── __main__.py
├── .env
├── Dockerfile
├── init_db.py
├── LICENSE
├── README.md
├── requirements.txt

### Each File Explained

### Difficulties Met