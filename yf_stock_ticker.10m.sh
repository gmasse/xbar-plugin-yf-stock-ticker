#!/bin/sh
# <xbar.title>YF Stock Ticker</xbar.title>
# <xbar.version>v0.1beta</xbar.version>
# <xbar.author>Germain Masse</xbar.author>
# <xbar.author.github>gmasse</xbar.author.github>
# <xbar.desc>--Use Yahoo Finance data to monitor stock indices, currencies and cryptocurrencies</xbar.desc>
# <xbar.dependencies>python3</xbar.dependencies>
# <xbar.var>string(VAR_TICKER_SYMBOLS="AAPL BTC-USD"): Space delimited list of symbols to display in the status bar.</xbar.var>
# <xbar.var>string(VAR_DROPDOWN_SYMBOLS="AAPL ^IXIC ETH-BTC"): Space delimited list of symbols to display in the dropdown.</xbar.var>
#
# Yahoo Finance data retrieval rely on https://github.com/dpguthrie/yahooquery
# Greatly inspired by "Yahoo Stock Ticker" (@longpdo) and "bitbar-plugin-pingdom" (@infothrill)

SOURCE_URL="https://raw.githubusercontent.com/gmasse/xbar-plugin-yf-stock-ticker/main/yf_stock_ticker/yf_stock_ticker.py"
PLUGIN_NAME="yf_stock_ticker"
PACKAGES=(yahooquery)


PROGNAME=$(basename -- "$0")
SELF_PATH=$(cd -P -- "$(dirname -- "$0")" && pwd -P) && SELF_PATH=$SELF_PATH/$(basename -- "$0")
# resolve symlinks
while [ -h "$SELF_PATH" ]; do
    # 1) cd to directory of the symlink
    # 2) cd to the directory of where the symlink points
    # 3) get the pwd
    DIR=$(dirname -- "$SELF_PATH")
    SYM=$(readlink "$SELF_PATH")
    SELF_PATH=$(cd "$DIR" && cd "$(dirname -- "$SYM")" && pwd)
    PROGNAME=$(basename -- "$SYM")
done

error_exit()
{
    echo "${PROGNAME}: ${1:-"Unknown Error"}" 1>&2
    exit 1
}

PLUGIN_DIR="$(dirname "${SELF_PATH}")/${PLUGIN_NAME}"
if [ ! -d "${PLUGIN_DIR}" ]; then
    # source code directory does not exists, let's download the plugin
    mkdir -p "${PLUGIN_DIR}" || error_exit "mkdir -p ${PLUGIN_DIR}"
    curl -s -o "${PLUGIN_DIR}/${PLUGIN_NAME}.py" "${SOURCE_URL}" || error_exit "curl error"
    chmod +x "${PLUGIN_DIR}/${PLUGIN_NAME}.py" || error_exit "chmod +x"
fi

cd "${PLUGIN_DIR}" || error_exit "cd ${PLUGIN_DIR}"
if [ -d "venv" ]; then
    source venv/bin/activate || error_exit "venv activation"
else
    # no python virtual environment found, let's create one and install dependencies
    python3 -m venv venv || error_exit "venv creation"
    source venv/bin/activate || error_exit "venv activation"
    python3 -m pip install -U pip wheel || error_exit "pip upgrade"
    for package in "${PACKAGES[@]}"; do
        python3 -m pip install ${package} || error_exit "package ${package}"
    done
fi

exec "${PLUGIN_DIR}/${PLUGIN_NAME}.py"
