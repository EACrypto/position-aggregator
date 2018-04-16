import requests
import json
import datetime
import sys
from time import sleep

BASE_URI = "https://www.bitmex.com/api/v1/trade?"
COLS = "side%2C%20size%2C%20price"

def get_all_trades(instrument, start_time, end_time, page_num = 0):
    base_query_url = \
        BASE_URI + "symbol={}&columns={}&startTime={}&endTime={}&count=500" \
                        .format(instrument, COLS, start_time, end_time)

    query_url = base_query_url + "&start={}".format(page_num * 500)

    response = requests.get(query_url)
    if (response.ok):
        jData = json.loads(response.content.decode("utf-8"))
    else:
        print("Request error: {}".format(response))
        sys.exit()

    if len(jData) == 500:
        sleep(0.1)
        jData.extend(get_all_trades(instrument, start_time, end_time, page_num + 1))
    return jData

def agg_tradeflow(trades):
    total_buys = 0
    total_sells = 0
    for trade in trades:
        if trade['side'] == 'Buy':
            total_buys += trade['size']
        else:
            total_sells += trade['size']
    return (total_buys, total_sells)

if __name__ == '__main__':
    instrument = "XBT"
    start_time = "2018-04-15%2020%3A05%3A00"
    end_time = str(datetime.datetime.now())
    jData = get_all_trades(instrument, start_time, end_time)
    buys, sells = agg_tradeflow(jData)
    print("B: {:,}".format(buys))
    print("S: {:,}".format(sells))
