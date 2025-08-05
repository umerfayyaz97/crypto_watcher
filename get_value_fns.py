
def schedule_interval_check():
    "This function confirm choice for Interval for Charts, 1 minutes, 5 minutes, 10 minutes 15 minutes, 30 minutes"
    interval = input("Enter time Interval for Chart in minutes e.g: 1 = 1 minute, 60 = 1 hour : \n Select from '1','5','10','15','30', '60', '120' only: \n" )
    while interval:
        if interval not in ['5', '10', '15', '30','1', '60' , '120' ]:
            print("Select from Given List only: \n")
            interval =  input("Enter Again: \n")
        else:
            return int(interval)
 

def currency_pair():
    "This function confirms currency to watch in Pair value ensuring a single '/' separator"
    pair = input("Enter currency in pair value only, e.g: BNB/USDT, ETH/BTC, BNB/ETH etc: \n  input:   ")
    while pair:
        if pair.count('/') != 1:
            print("Invalid format. \n")
            pair = input("Use exactly onle one '/' to separate currency pairs: \n input:  ")
            continue
        else:
            pass

        parts = pair.split('/')

        base_currency = parts[0].lower().strip() # Convert to lowercase
        quote_currency = parts[1].lower().strip() 

        joined_pairs = base_currency + quote_currency
       
        return joined_pairs.upper()
                
def exchange_name():
    "This function confirms exchange name from given list"
    exchanges_list: str = ['Binance','OKX','Bybit','Bitget']

    lowercase_exchange = [exchange.lower() for exchange in exchanges_list]
    
    selected_exchange = input(f"Chose Exchange from {exchanges_list} \n input: ").lower().strip()
    while selected_exchange:
        if selected_exchange not in lowercase_exchange:
            print("Wrong Selection, chose only given options \n")
            selected_exchange = input("Input:  ").lower()
            continue
        else:
            return selected_exchange.upper()

    


def screenshot_interval(interval):
    """
    This function takes a time interval string (e.g., '1m', '5m')
    and converts it into the equivalent number of seconds.
    It handles 1m, 5m, 10m, 15m, 30m, 60m and 120m  intervals.
    """
   
    if interval == 1:
            time_in_seconds = 1 * 60  # 1 minute * 60 seconds/minute
    elif interval == 5:
            time_in_seconds = 5 * 60  # 5 minutes * 60 seconds/minute
    elif interval == 10:
            time_in_seconds = 10 * 60 # 10 minutes * 60 seconds/minute
    elif interval == 15:
            time_in_seconds = 15 * 60 # 15 minutes * 60 seconds/minute
    elif interval == 30:
            time_in_seconds = 30 * 60 # 30 minutes * 60 seconds/minute
    elif interval == 60: # Added 60 minute conversion
        time_in_seconds = 60 * 60
    elif interval == 120: # Added 120 minute conversion
        time_in_seconds = 120 * 60
    else:
        time_in_seconds = 0 
    return time_in_seconds



# def construct_url():
#     "This function construct URL for trading view with selected exchanges and pair with specific timeframe. "

#     interval = schedule_interval_check() # get time interval for charts in minutes
#     exchange = exchange_name() # get exchange
#     pair = currency_pair() # get currency pair

#     url = f"https://www.tradingview.com/chart/?symbol={exchange}%3A{pair}&interval={interval}"
    
#     return url


def construct_url(exchange, pair, interval):
    """
    This function constructs a TradingView URL from provided components.
    """
    url = f"https://www.tradingview.com/chart/?symbol={exchange}%3A{pair}&interval={interval}"
    return url