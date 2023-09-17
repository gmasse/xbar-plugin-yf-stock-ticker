#!/usr/bin/env LC_ALL=en_US.UTF-8 python3

import os
import logging

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
logging.basicConfig(format=FORMAT, level=logging.WARNING)
log = logging.getLogger()


def get_quotes(symbols):
    quotes = Ticker(symbols)
    data = quotes.price
    for symbol in symbols:
        if not isinstance(data[symbol], dict):
            log.warning("Quote not found for symbol: %s", symbol)
            del(data[symbol])
    return data


def print_ticker(symbol_data):
    symbol = ''
    if symbol_data['quoteType'] == 'CURRENCY':
        symbol = symbol_data['shortName']
    else:
        symbol = symbol_data['symbol'].split('.')[0] # Remove appending stock exchange symbol for foreign exchanges, e.g. Apple stock symbol in Frankfurt: APC.F -> AP

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
    print('{}{} {:.2%}{}'.format(prefix, symbol, symbol_data['regularMarketChangePercent'], suffix))


def print_dropdown(symbol_data):
    FONT = " | font='Menlo'"

    symbol = ''
    if symbol_data['quoteType'] == 'CURRENCY':
        symbol = symbol_data['shortName']
    else:
        # Remove appending stock exchange symbol for foreign exchanges, e.g. Apple stock symbol in Frankfurt: APC.F -> APC
        symbol = symbol_data['symbol'].split('.')[0]

    suffix = ''
    if symbol_data['marketState'] != 'REGULAR':
        suffix = '🌘'
    elif symbol_data['regularMarketChangePercent'] > 0:
        suffix = '🟢'
    elif symbol_data['regularMarketChangePercent'] < 0:
        suffix = '🔴'
    else:
        suffix = '🟰'
    formated_change = '{:+.2%}'.format(symbol_data['regularMarketChangePercent'])
    regularMarketPrice = '{:.2f}'.format(symbol_data['regularMarketPrice'])
    print("{:<7} {:>10} {:>10} {}".format(symbol, regularMarketPrice, formated_change, suffix) + FONT)

    print("--{} ({})".format(symbol_data['longName'], symbol_data['currency']) + FONT)
    print("--Previous Close: {:.2f}".format(symbol_data['regularMarketPreviousClose']) + FONT)
    print("--Open:           {:.2f}".format(symbol_data['regularMarketOpen']) + FONT)
    print("--Day's Range:    {:.2f} - {:.2f}".format(symbol_data['regularMarketDayLow'], symbol_data['regularMarketDayHigh']) + FONT)


if __name__ == '__main__':
    unique_symbols = SYMBOLS_TICKER + list(set(SYMBOLS_DROPDOWN) - set(SYMBOLS_TICKER))
    quotes = get_quotes(unique_symbols)

    if len(SYMBOLS_TICKER) == 0:
        print("xbar")
    else:
        for symbol in SYMBOLS_TICKER:
            if symbol in quotes:
                data = quotes[symbol]
                print_ticker(data)

    print("---")

    for symbol in SYMBOLS_DROPDOWN:
        if symbol in quotes:
            data = quotes[symbol]
            print_dropdown(data)
