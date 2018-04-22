import requests
import json
import datetime
import sys
from time import sleep

BASE_URI = "https://www.bitmex.com/api/v1/trade?"
COLS = "side%2C%20size%2C%20price"

def get_all_trades(instrument, start_time, end_time, page_num = 0):
    print("Working on page {}...".format(str(page_num)))
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
    time_delta = datetime.timedelta(minutes = 240)
    end_time = datetime.datetime.utcnow()
    start_time = end_time - time_delta
    # start_time = "2018-04-14 13:00:00"
    # end_time = "2018-04-15 20:00:00"

    data = []
    new_data = get_all_trades(instrument, str(start_time), str(end_time))
    data.extend(new_data)
    page_num = 0
    while len(new_data) == 500:
        sleep(1.5)
        page_num += 1
        new_data = get_all_trades(instrument, start_time, end_time, page_num)
        data.extend(new_data)

    buys, sells = agg_tradeflow(data)
    print("Start Time: {}".format(str(start_time)))
    print("End Time: {}".format(str(end_time)))
    print("B: {:,}".format(buys))
    print("S: {:,}".format(sells))
