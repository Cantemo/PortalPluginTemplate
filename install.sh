#!/bin/bash
PORTAL_ROOT="/opt/cantemo/portal"
PLUGIN_NAME="PortalPluginTemplate"

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ "X${DIR}" = "X" ]; then
    echo "Error: Could not figure out your source directory. This should not happen."
    exit 1
fi

sudo mkdir -p $PORTAL_ROOT/portal/plugins/$PLUGIN_NAME
sudo cp -r $DIR/* $PORTAL_ROOT/portal/plugins/$PLUGIN_NAME

echo "Done."
echo "Stop Portal: supervisorctl stop portal"
echo "Sync the database: root@mediabox:/opt/cantemo/portal# python manage.py syncdb"
echo "Start Portal: supervisorctl start portal"
