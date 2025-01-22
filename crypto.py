#!/usr/bin/env python3

import requests
import sys
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Your CoinMarketCap API key
API_KEY = 'enter_api_key_here'

# News API Key
NEWS_API_KEY = 'enter_api_key_here'

# URLs
COINMARKETCAP_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
TOP_CRYPTO_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
FGI_URL = 'https://api.alternative.me/fng/'
NEWS_URL = 'https://newsapi.org/v2/everything'

# Check for user input
if len(sys.argv) < 2:
    print(Fore.RED + "Usage: crypto <symbol> [vol|mk|news|fgi|convert <from_symbol> <to_symbol> <amount>]")
    sys.exit(1)

# Parse command-line arguments
args = [arg.lower() for arg in sys.argv[1:]]
symbols = [arg.upper() for arg in args if arg not in ["vol", "mk", "news", "fgi", "convert"]]
show_volume = "vol" in args
show_market_cap = "mk" in args
show_news = "news" in args
show_fgi = "fgi" in args
conversion = "convert" in args

# Detect 'topXX' command
top_limit = None
for arg in args:
    if arg.startswith("top"):
        try:
            top_limit = int(arg[3:])  # Extract the number after 'top'
        except ValueError:
            print(Fore.RED + "Invalid 'top' command. Use 'topXX' (e.g., 'top10').")
            sys.exit(1)

# Function to fetch cryptocurrency data
def fetch_data(symbols=None):
    headers = {'X-CMC_PRO_API_KEY': API_KEY, 'Accept': 'application/json'}
    if symbols:
        symbols_query = ','.join(symbols)
        response = requests.get(f'{COINMARKETCAP_URL}?symbol={symbols_query}&convert=USD', headers=headers)
    else:
        response = requests.get(f'{COINMARKETCAP_URL}?convert=USD', headers=headers)
    return response.json() if response.status_code == 200 else None

# Function to fetch cryptocurrency news
def fetch_news(query=None):
    params = {
        'apiKey': NEWS_API_KEY,
        'q': query if query else 'cryptocurrency',
        'language': 'en',
        'sortBy': 'publishedAt'
    }
    response = requests.get(NEWS_URL, params=params)
    return response.json() if response.status_code == 200 else None

# Function to fetch the Fear and Greed Index (FGI)
def fetch_fgi():
    response = requests.get(FGI_URL)
    if response.status_code == 200:
        data = response.json()
        if 'data' in data:
            fgi_value = data['data'][0]['value']
            fgi_text = data['data'][0]['value_classification']
            return fgi_value, fgi_text
    return None, None

# Function to fetch conversion rates
def fetch_conversion_rate(from_symbol, to_symbol):
    headers = {'X-CMC_PRO_API_KEY': API_KEY, 'Accept': 'application/json'}
    response = requests.get(f'{COINMARKETCAP_URL}?symbol={from_symbol},{to_symbol}&convert=USD', headers=headers)
    if response.status_code == 200:
        data = response.json()
        from_price = data['data'][from_symbol]['quote']['USD']['price']
        to_price = data['data'][to_symbol]['quote']['USD']['price']
        conversion_rate = from_price / to_price
        return conversion_rate
    return None

# Handle conversion command
if conversion:
    try:
        from_symbol = args[args.index("convert") + 1].upper()
        to_symbol = args[args.index("convert") + 2].upper()
        amount = float(args[args.index("convert") + 3])

        conversion_rate = fetch_conversion_rate(from_symbol, to_symbol)
        if conversion_rate is not None:
            converted_amount = amount * conversion_rate
            print(Fore.CYAN + f"\nConversion:")
            print(Fore.MAGENTA + f"  - {amount} {from_symbol} = {converted_amount:.6f} {to_symbol}")
        else:
            print(Fore.RED + "Failed to fetch conversion rates.")
    except (IndexError, ValueError):
        print(Fore.RED + "Invalid conversion command. Usage: convert <from_symbol> <to_symbol> <amount>")

# Fetch top cryptocurrencies if 'topXX' is detected
if top_limit:
    print(Fore.CYAN + f"\nTop {top_limit} Cryptocurrencies:")
    headers = {'X-CMC_PRO_API_KEY': API_KEY, 'Accept': 'application/json'}
    params = {'limit': top_limit, 'convert': 'USD'}
    response = requests.get(TOP_CRYPTO_URL, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        for coin_data in data['data']:
            symbol = coin_data['symbol']
            name = coin_data['name']
            price = coin_data['quote']['USD']['price']
            volume = coin_data['quote']['USD']['volume_24h']
            market_cap = coin_data['quote']['USD']['market_cap']
            
            print(Style.BRIGHT + Fore.MAGENTA + f"\n{name} ({symbol}):")
            print(Style.BRIGHT + Fore.MAGENTA + f"  - Price: " + Fore.GREEN + f"${price:.10f}")
            print(Style.BRIGHT + Fore.MAGENTA + f"  - 24h Volume: " + Fore.GREEN + f"${volume:,.2f}")
            print(Style.BRIGHT + Fore.MAGENTA + f"  - Market Cap: " + Fore.GREEN + f"${market_cap:,.2f}")
    else:
        print(Fore.RED + f"Failed to fetch top {top_limit} cryptocurrencies.")

# Fetch data for requested symbols (only show for non-conversion requests)
if symbols and not conversion:
    data = fetch_data(symbols)
    if data:
        print(Fore.CYAN + "\nCrypto Data:")
        for symbol in symbols:
            if symbol in data['data']:
                coin_data = data['data'][symbol]
                price = coin_data['quote']['USD']['price']
                volume = coin_data['quote']['USD']['volume_24h']
                market_cap = coin_data['quote']['USD']['market_cap']

                print(Style.BRIGHT + Fore.MAGENTA + f"\n{symbol}:")
                print(Style.BRIGHT + Fore.MAGENTA + f"  - Price: " + Fore.GREEN + f"${price:.10f}")
                if show_volume:
                    print(Style.BRIGHT + Fore.MAGENTA + f"  - 24h Volume: " + Fore.GREEN + f"${volume:,.2f}")
                if show_market_cap:
                    print(Style.BRIGHT + Fore.MAGENTA + f"  - Market Cap: " + Fore.GREEN + f"${market_cap:,.2f}")
    else:
        print(Fore.RED + f"Failed to fetch data for {', '.join(symbols)}.")

# Fetch and display FGI if requested
if show_fgi:
    fgi_value, fgi_text = fetch_fgi()
    if fgi_value is not None:
        print(Fore.CYAN + f"\nFear and Greed Index: {fgi_value}")
        print(Fore.GREEN + f"  Classification: {fgi_text}")
    else:
        print(Fore.RED + "Failed to fetch Fear and Greed Index.")

# Fetch cryptocurrency news if requested
if show_news:
    articles = fetch_news(query=None)
    if articles:
        print(Fore.CYAN + "\nLatest Crypto News:")
        for article in articles['articles'][:5]:  # Limit to top 5 news articles
            title = article['title']
            url = article['url']
            description = article['description']
            print(Fore.MAGENTA + f"  - {title}")
            print(Fore.GREEN + f"    {description}")
            print(Fore.CYAN + f"    Read more: {url}\n")
    else:
        print(Fore.RED + "Failed to fetch news.")

# Fetch news for a specific symbol if requested
if len(symbols) == 1 and len(args) > 1 and args[1] == "news":
    symbol = symbols[0]
    articles = fetch_news(query=symbol)
    if articles:
        print(Fore.CYAN + f"\nLatest News for {symbol.upper()}:")
        for article in articles['articles'][:5]:  # Limit to top 5 news articles
            title = article['title']
            url = article['url']
            description = article['description']
            print(Fore.MAGENTA + f"  - {title}")
            print(Fore.GREEN + f"    {description}")
            print(Fore.CYAN + f"    Read more: {url}\n")
    else:
        print(Fore.RED + f"Failed to fetch news for {symbol.upper()}.")
