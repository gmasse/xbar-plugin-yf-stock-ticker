#!/bin/sh
# <xbar.title>YF Stock Ticker</xbar.title>
# <xbar.version>v0.4-beta</xbar.version>
# <xbar.author>Germain Masse</xbar.author>
# <xbar.author.github>gmasse</xbar.author.github>
# <xbar.desc>--Use Yahoo Finance data to monitor stock indices, currencies and cryptocurrencies</xbar.desc>
# <xbar.dependencies>python3</xbar.dependencies>
# <xbar.var>string(VAR_TICKER_SYMBOLS="AAPL BTC-USD"): Space delimited list of symbols to display in the status bar.</xbar.var>
# <xbar.var>string(VAR_DROPDOWN_SYMBOLS="AAPL ^IXIC ETH-BTC"): Space delimited list of symbols to display in the dropdown.</xbar.var>
# <xbar.var>boolean(VAR_AUTO_UPDATE=true): Check and update plugin automatically.</xbar.var>
#
# Yahoo Finance data retrieval rely on https://github.com/dpguthrie/yahooquery
# Greatly inspired by "Yahoo Stock Ticker" (@longpdo) and "bitbar-plugin-pingdom" (@infothrill)

set -e

if [ "${DEBUG}" = true ]; then
    set -x
    #TODO: increase verbosity for pip and tar
fi

GITHUB_REPO="gmasse/xbar-plugin-yf-stock-ticker"
PLUGIN_NAME="yf_stock_ticker"

PYTHON_SCRIPT="${PLUGIN_NAME}.py"
SHELL_WRAPPER="${PLUGIN_NAME}.sh"

CURRENT_VERSION=$(grep '^# *<xbar.version>' "$0" | sed -E 's/.*<xbar.version>([^<]+)<\/xbar.version>.*/\1/')
INSTALL_TODO=false

get_latest_version()
{
    LATEST_VERSION=$(curl --silent "https://api.github.com/repos/${GITHUB_REPO}/releases/latest" | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/')
}

if [ "$1" = '-v' ] || [ "$1" = '--version' ]; then
    # print version and exit
    echo "${CURRENT_VERSION}"
    exit 0
fi

# check if plugin is installed
PROGNAME=$(basename -- "$0")
SELF_PATH=$(cd -P -- "$(dirname -- "$0")" && pwd -P) && SELF_PATH=$SELF_PATH/$(basename -- "$0")
# resolve symlinks in case the plugin in installed in a non usual location
while [ -h "$SELF_PATH" ]; do
    # 1) cd to directory of the symlink
    # 2) cd to the directory of where the symlink points
    # 3) get the pwd
    DIR=$(dirname -- "$SELF_PATH")
    SYM=$(readlink "$SELF_PATH")
    SELF_PATH=$(cd "$DIR" && cd "$(dirname -- "$SYM")" && pwd)
done

PLUGIN_DIR="$(dirname "${SELF_PATH}")/${PLUGIN_NAME}"
if [ ! -d "${PLUGIN_DIR}" ]; then
    # source code directory does not exist, installation required
    get_latest_version
    if [ -z "${LATEST_VERSION}" ]; then
        >&2 echo "Unable to get the latest version number"
    else
        # force install
        INSTALL_TODO=true
    fi
else
    # plugin already installed, autoupdate?
    if [ "${VAR_AUTO_UPDATE}" = 'true' ]; then
        # get the latest version (release tag name)
        get_latest_version
        if [ -z "${LATEST_VERSION}" ]; then
            >&2 echo "Unable to check the latest version"
        else
            if [ "${LATEST_VERSION}" != "${CURRENT_VERSION}" ]; then
                # versions mismatch, update is required
                INSTALL_TODO=true
            fi
        fi
    fi
fi

error_exit()
{
    echo "${PROGNAME}: ${1:-"Unknown Error"}" 1>&2
    exit 1
}

if [ ${INSTALL_TODO} = true ]; then
    curl --silent --location "https://github.com/${GITHUB_REPO}/releases/download/${LATEST_VERSION}/${PLUGIN_NAME}_${LATEST_VERSION}.tgz" | tar zx || error_exit "installation"
    ln -sf "${PLUGIN_DIR}/${SHELL_WRAPPER}" "${PROGNAME}" || error_exit "ln -sf ${PLUGIN_DIR}/${SHELL_WRAPPER} ${PROGNAME}"
fi

# install or update dependencies
cd "${PLUGIN_DIR}" || error_exit "cd ${PLUGIN_DIR}"
if [ ! -d "venv" ]; then
    python3 -m venv venv || error_exit "venv creation"
    INSTALL_TODO=true
fi
# shellcheck disable=SC1091
. venv/bin/activate || error_exit "venv activation"

# check installed packages
if ! python3 -c "import pkg_resources; pkg_resources.require(open('requirements.txt',mode='r'))"; then
    # requirements unsatisfied, need to reinstall
    INSTALL_TODO=true
fi

# install packages if needed
if [ "${INSTALL_TODO}" = true ]; then
    # installation or update required
    # update pip and install wheel package
    python3 -m pip -q install -U pip wheel || error_exit "pip upgrade"
    # install required packages
    python3 -m pip -q install -r requirements.txt || error_exit "pip install -r requirements.txt"
fi

exec "${PLUGIN_DIR}/${PYTHON_SCRIPT}"
