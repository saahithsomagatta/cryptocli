# cryptocli
A lightweight cli for linux for crypto functionality
some good features, but need to add some more
feel free to request some!

# features
- get real-time cryptocurrency price, volume, and market cap
- fetch cryptocurrency news
- check the current fear and greed index (FGI)

## Prerequisites
Before using the script, you need to have API keys for the following services:
- **CoinMarketCap** for cryptocurrency data.
- **NewsAPI** for cryptocurrency news.
- **Requests** for sending get requests.
- **Colorama** for rgb text omg so gamer.

### 1. Get a CoinMarketCap API Key
- Sign up at [CoinMarketCap](https://coinmarketcap.com/api/) and get your free API key.

### 2. Get a NewsAPI Key
- Sign up at [NewsAPI](https://newsapi.org/) and get your free API key.

### 3. Install Requests and Colorama
- on debian and ubuntu go to terminal.
- make sure you have python installed and run these scripts
- `sudo apt install python3-requests`
- `sudo apt install python3-colorama`

## Downloading and Setting up
- download crypto.py
- open the file with a text editor and replace the text on line 11 (enter_api_key_here) with your api key for CMC
- open the file with a text editor and replace the text on line 14 (enter_api_key_here) with your api key for NewsAPI
- run this in terminal to move the script to /usr/local/bin
- `sudo mv crypto.py /usr/local/bin/crypto`
- then run this to make it an executable
- `sudo chmod +x /usr/local/bin/crypto`
- open terminal and run crypto
- something along the signs of `Usage: crypto <symbol> [vol|mk|news|fgi]` should show up

## How to use
- `crypto xxx`
grabs xxx's price (enter whatever crypto ticker you want in xxx)
- `crypto xxx yyy`
grabs xxx's price and yyy's price
- `crypto xxx vol`
grabs xxx's market volume for the past 24 hours
- `crypto xxx mk`
grabs the market cap for xxx
- `crypto xxx news`
grabs the latest articles about xxx
- `crypto news`
grabs the latest crypto news
- `crypto fgi`
grabs the FGI (Fear and Greed Index)
- `crypto topxx`
grabs the top xx cryptos by marketcap (replace xx with whatever number you want)
- `crypto convert xxx yyy zzz`
convert zzz amount of crypto xxx to crypto yyy
