# EVM Visual

## License

This project is licensed under the GNU Lesser General Public License (LGPL) v3.0.
See the [LICENSE](./LICENSE) file for details.

### Setup
- Install *Graphviz* `sudo apt-get install graphviz graphviz-dev`. If you you problem installing it, follow the instructions [here](https://pygraphviz.github.io/documentation/stable/install.html).
- Install Graph-Tools `sudo apt-get install python3-graph-tool`


### Database of addresses
The database is an aggregation of the following sources:
- [Binance's Commitment to Transparency](https://www.binance.com/en/blog/community/our-commitment-to-transparency-2895840147147652626)
- [Etherscan](https://etherscan.io/accounts), for this source, there is no automation, as it is impossible to know if the addresses are malicious, or if the graph generation should stop when meeting one of them.
- [Ethereum List Repo](https://github.com/MyEtherWallet/ethereum-lists)
- [Kaggle Database by Hamish Hall](https://www.kaggle.com/datasets/hamishhall/labelled-ethereum-addresses)

Due to the fact that they come from several sources, there isn't a unique format. One by one, each source has been happend in a csv file with a new format, that fits the need of this project. Then, the csv is transformed into an actuall sqlite3 database when the Docker image is started.

##### Useful:
- Sepolia address source for simple graph: "0x2461214FC9777705b962248104a58f52BF41B3db"
- When meeting an address with a crazy number of transactions, which slows significantly the graph generation, it is recommended to reference this address, unchecking `Continue` so the the graph generation stops when meeting this address.