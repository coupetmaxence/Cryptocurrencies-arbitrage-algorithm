# Cryptocurrencies arbitrage algorithm

## Presentation

The main goal of this project is to use the important number of cryptocurrencies and cryptocurrencies' exchanges in order to detect gaps in the market.
We are focusing on three main arbitrages : simple arbitrage (ex : the paire BTC/USD with two different prices on two exchanges), triangular arbitrage ([wikipedia's explanation](https://en.wikipedia.org/wiki/Triangular_arbitrage)) and order book analysis (detecting imbalances between sell and buy sides).

We retrieve the datas of all exchanges via the webservice [coinigy](https://www.coinigy.com/)


## Prerequisites

This code is written in Python, so you will python 3.4 or higher on your computer. 
