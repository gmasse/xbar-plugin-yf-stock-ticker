import os
import sys
from yahooquery import Ticker
import yf_stock_ticker.yf_stock_ticker as yf_stock_ticker

os.environ['TZ'] = 'UTC' # set default timezone

sample_quote_data = {'AAPL': {'averageDailyVolume10Day': {},
                              'averageDailyVolume3Month': {},
                              'circulatingSupply': {},
                              'currency': 'USD',
                              'currencySymbol': '$',
                              'exchange': 'NMS',
                              'exchangeDataDelayedBy': 0,
                              'exchangeName': 'NasdaqGS',
                              'fromCurrency': None,
                              'lastMarket': None,
                              'longName': 'Apple Inc.',
                              'marketCap': 2732701515776,
                              'marketState': 'CLOSED',
                              'maxAge': 1,
                              'openInterest': {},
                              'postMarketChange': 0.16000366,
                              'postMarketChangePercent': 0.00091540517,
                              'postMarketPrice': 174.95,
                              'postMarketSource': 'DELAYED',
                              'postMarketTime': '2023-09-22 23:59:53',
                              'preMarketChange': {},
                              'preMarketPrice': {},
                              'preMarketSource': 'FREE_REALTIME',
                              'priceHint': 2,
                              'quoteSourceName': 'Delayed Quote',
                              'quoteType': 'EQUITY',
                              'regularMarketChange': 0.8600006,
                              'regularMarketChangePercent': 0.0049445215,
                              'regularMarketDayHigh': 177.079,
                              'regularMarketDayLow': 174.055,
                              'regularMarketOpen': 174.67,
                              'regularMarketPreviousClose': 173.93,
                              'regularMarketPrice': 174.79,
                              'regularMarketSource': 'FREE_REALTIME',
                              'regularMarketTime': '2023-09-22 20:00:02',
                              'regularMarketVolume': 55110610,
                              'shortName': 'Apple Inc.',
                              'strikePrice': {},
                              'symbol': 'AAPL',
                              'toCurrency': None,
                              'underlyingSymbol': None,
                              'volume24Hr': {},
                              'volumeAllCurrencies': {}}}


def test_get_quotes(monkeypatch):
    def mock_quote_summary(*args, **kwargs):
        output = sample_quote_data
        output['UNKNOW'] = 'Quote not found for ticker symbol: UNKNOWN'
        return output;

    monkeypatch.setattr(Ticker, "_quote_summary", mock_quote_summary)
    assert yf_stock_ticker.get_quotes(['AAPL']) == sample_quote_data


def test_gen_ticker(capsys):
    assert yf_stock_ticker.gen_ticker(sample_quote_data['AAPL']) == "☾ AAPL 0.49%\n"


def test_gen_drodpdown(capsys):
    assert yf_stock_ticker.gen_dropdown(sample_quote_data['AAPL']) == \
"""AAPL        174.79     +0.49% 🌘 | font='Menlo'
--Apple Inc. (USD) | font='Menlo'
--Previous Close: 173.93 | font='Menlo'
--Open:           174.67 | font='Menlo'
--Day's Range:    174.06 - 177.08 | font='Menlo'
"""
