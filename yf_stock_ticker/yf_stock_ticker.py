#!/usr/bin/env LC_ALL=en_US.UTF-8 python3
""" xbar plugin
    --Use Yahoo Finance data to monitor stock indices, currencies and cryptocurrencies """

import sys
import os
import logging

import requests.exceptions
from yahooquery import Ticker


SYMBOLS_TICKER = []
SYMBOLS_DROPDOWN = []
# user defined list of stock to display (in the navbar or in the dropdown)
# space delimited environment variables are converted to list (removing empty elements)
if os.environ.get('VAR_TICKER_SYMBOLS') is not None:
    SYMBOLS_TICKER = list(filter(None, os.environ.get('VAR_TICKER_SYMBOLS').split(' ')))
if os.environ.get('VAR_DROPDOWN_SYMBOLS') is not None:
    SYMBOLS_DROPDOWN = list(filter(None, os.environ.get('VAR_DROPDOWN_SYMBOLS').split(' ')))


# Enable debug
FORMAT = ('%(asctime)-15s %(threadName)-15s '
          '%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
if os.environ.get('DEBUG') == 'true':
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)
else:
    logging.basicConfig(format=FORMAT, level=logging.WARNING)
log = logging.getLogger()


def get_quotes(symbols):
    """ Get quotes with yahooquery """

    try:
        quotes = Ticker(symbols)
        data = quotes.price
    except requests.exceptions.ConnectionError:
        log.warning("Cannot get data")
        return None

    if 'error' in data:
        log.warning("Yahooquery failure: %s", data['error'])
    else:
        for symbol in symbols:
            if not isinstance(data[symbol], dict):
                log.warning("Quote not found for symbol: %s", symbol)
                del data[symbol]
    return data


def gen_ticker(symbol_data):
    """ Display a quote on the navbar """

    symbol = ''
    if symbol_data['quoteType'] == 'CURRENCY':
        symbol = symbol_data['shortName']
    else:
        symbol = symbol_data['symbol'].split('.')[0] # Remove appending stock exchange symbol for
                                                     # foreign exchanges, e.g. Apple stock symbol
                                                     # in Frankfurt: APC.F -> APC

    prefix = ''
    suffix = ''
    if symbol_data['marketState'] != 'REGULAR':
        prefix = '☾ '
    elif symbol_data['regularMarketChangePercent'] > 0:
        prefix = '▲ '
        suffix = ' | color=green'
    elif symbol_data['regularMarketChangePercent'] < 0:
        prefix = '▼ '
        suffix = ' | color=red'
    else:
        prefix = '= '
    return f"{prefix}{symbol} {symbol_data['regularMarketChangePercent']:.2%}{suffix}\n"


def gen_dropdown(symbol_data):
    """ Display a quote in the dropdown """

    FONT = " | font='Menlo'" # pylint: disable=invalid-name

    output = ''
    symbol = ''
    if symbol_data['quoteType'] == 'CURRENCY':
        symbol = symbol_data['shortName']
    else:
        symbol = symbol_data['symbol'].split('.')[0] # Remove appending stock exchange symbol for
                                                     # foreign exchanges, e.g. Apple stock symbol
                                                     # in Frankfurt: APC.F -> APC

    suffix = ''
    if symbol_data['marketState'] != 'REGULAR':
        suffix = '🌘'
    elif symbol_data['regularMarketChangePercent'] > 0:
        suffix = '🟢'
    elif symbol_data['regularMarketChangePercent'] < 0:
        suffix = '🔴'
    else:
        suffix = '🟰'
    formated_change = f"{symbol_data['regularMarketChangePercent']:+.2%}"
    regular_market_price = f"{symbol_data['regularMarketPrice']:.2f}"

    output += f"{symbol:<7} {regular_market_price:>10} {formated_change:>10} {suffix}" + FONT + "\n"
    output += f"--{symbol_data['longName']} ({symbol_data['currency']})" + FONT + "\n"
    output += f"--Previous Close: {symbol_data['regularMarketPreviousClose']:.2f}" + FONT + "\n"
    output += f"--Open:           {symbol_data['regularMarketOpen']:.2f}" + FONT + "\n"
    output += f"--Day's Range:    {symbol_data['regularMarketDayLow']:.2f}" \
           + f" - {symbol_data['regularMarketDayHigh']:.2f}" + FONT + "\n"
    return output

def main():
    """ Main function """

    unique_symbols = SYMBOLS_TICKER + list(set(SYMBOLS_DROPDOWN) - set(SYMBOLS_TICKER))
    quotes = get_quotes(unique_symbols)

    if quotes is None:
        print("⚠️ connection failed | color=gray")
        sys.exit(0)

    if len(SYMBOLS_TICKER) == 0:
        print("xbar")
    else:
        for symbol in SYMBOLS_TICKER:
            if symbol in quotes:
                data = quotes[symbol]
                print(gen_ticker(data), end='')

    print("---")

    for symbol in SYMBOLS_DROPDOWN:
        if symbol in quotes:
            data = quotes[symbol]
            print(gen_dropdown(data), end='')


if __name__ == '__main__':
    main()
