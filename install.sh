#!/bin/bash
PORTAL_ROOT="/opt/cantemo/portal"
PLUGIN_NAME="PortalPluginTemplate"

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ "X${DIR}" = "X" ]; then
    echo "Error: Could not figure out your source directory. This should not happend."
    exit 1
fi

sudo mkdir -p $PORTAL_ROOT/plugins/$PLUGIN_NAME
sudo cp -r $DIR/* $PORTAL_ROOT/plugins/$PLUGIN_NAME
