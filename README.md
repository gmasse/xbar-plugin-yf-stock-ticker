# xbar-plugin-yf-stock-ticker
![CI workflow](https://github.com/gmasse/xbar-plugin-yf-stock-ticker/actions/workflows/ci.yml/badge.svg)
[![GitHub Release](https://img.shields.io/github/release/gmasse/xbar-plugin-yf-stock-ticker.svg?style=flat)](https://github.com/gmasse/xbar-plugin-yf-stock-ticker/releases)

A (yet another) [xbar](https://xbarapp.com) plugin that display stock quotes, global indices, currencies and cryptocurrencies.
It does not require any account creation or API key. Data collection is made reliable thanks to [yahooquery](https://yahooquery.dpguthrie.com) package.

![Screenshot of the plugin](/assets/screenshot2_yf_stock_sticker.png)

The plugin accepts all the symbols supported by Yahoo! Finance.

## Features
- Market changes (%) will cycle in the navigation bar
- Market prices details will appear in the dropdown menu (symbols may be different from those in the navigation bar)
- Any Yahoo! Finance ticker symbol is supported:
  - stock (ex. `AAPL`)
  - index (ex. `^IXIC`)
  - FX rate (ex. `EURUSD=X`)
  - Cryptocurrency (ex. `BTC-USD`)
- Plugin automatic update (for ex. in case of YF breaking change, a plugin update will trigger the yahooquery package update)
- Configuration (symbols, auto-update) via plugin preferences panel

## Manual installation
In a terminal:
```sh
cd ~/Library/Application\ Support/xbar/plugins
curl -o yf_stock_ticker.10m.sh https://raw.githubusercontent.com/gmasse/xbar-plugin-yf-stock-ticker/main/yf_stock_ticker/yf_stock_ticker.sh
chmod +x yf_stock_ticker.10m.sh
```

## Configuration
Symbols to display can be configured in the xbar menu `Plugin Browser...`

![Screenshot of the plugin browser](/assets/screenshot_xbar_plugin_browser.png)

## Disclaimer
This project is not affiliated with Yahoo, Inc.

## Thanks
This plugin is greatly inspired by [Yahoo Stock Ticker](https://github.com/longpdo/bitbar-plugins-custom#yahoo-stock-ticker) and [bitbar-plugin-pingdom](https://github.com/infothrill/bitbar-plugin-pingdom).
