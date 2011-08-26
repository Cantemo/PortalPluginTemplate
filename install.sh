#!/bin/bash
PORTAL_ROOT="/opt/cantemo/portal"
PLUGIN_NAME="PortalPluginTemplate"
sudo mkdir -p $PORTAL_ROOT/portal/plugins/$PLUGIN_NAME
sudo mkdir -p $PORTAL_ROOT/portal_themes/core/templates/plugins/$PLUGIN_NAME

sudo cp *.py $PORTAL_ROOT/portal/plugins/$PLUGIN_NAME
sudo cp templates/* $PORTAL_ROOT/portal_themes/core/templates/plugins/$PLUGIN_NAME
