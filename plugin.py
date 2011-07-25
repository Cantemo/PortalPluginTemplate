from portal.pluginbase.core import *
from portal.generic.plugin_interfaces import IPluginURL, IPluginBlock
from django.template import loader, Context

import logging
log = logging.getLogger(__name__)

'''
URL Plugin that defines new URL's in the system
''' 
class MyPluginURL(Plugin):
    """ Loads the Admin rules URL's
    """
    implements(IPluginURL)
    
    def __init__(self):
        self.name = "MyPluginURL"
        # Should point to the urls.py
        self.urls = 'PortalPluginTemplate.urls'
        # Defines the URL pattern prefix
        self.urlpattern = r'^myplugin/'
        # Defines the plugin namespace
        self.namespace = 'myplugin'
        # Define a GUID for each plugin.
        # Use e.g. http://www.guidgenerator.com/
        self.plugin_guid = "replace-with-guid"
        log.debug("Initiated MyPluginURL")

# Load the URL plugin
pluginurls = MyPluginURL()

'''
Block plugin which defines new functionalities and workflows in to the system
'''
class MyPluginBlock(Plugin):
    
    implements(IPluginBlock)

    def __init__(self):
        # The name of the plugin which should match the pluginblock tag in the Portal template
        # For instance as defined in base_admin.html: {% pluginblock "AdminLeftPanelBottomPanePlugin" sand %}
        # This plugin is placed in the Admin page, in the left panel at the bottom
        self.name = "AdminLeftPanelBottomPanePlugin"
        # Define a GUID for each plugin.
        # Use e.g. http://www.guidgenerator.com/
        self.plugin_guid = "replace-with-guid"
        log.debug("Initiated MyPluginBlock")

    def return_string(self, tagname, *args):
        try:
            # Get the given theme
            theme = args[0][2]
        except:
            # fallback to sand theme
            theme = 'sand'
        return {'guid':self.plugin_guid, 'template':'%s/templates/plugins/PortalPluginTemplate/admin_leftpanel_entry.html' % theme}

pluginblock = MyPluginBlock() 

class MyNavBarPlugin(Plugin):
    
    implements(IPluginBlock)

    def __init__(self):
        # The name of the plugin which should match the pluginblock tag in the Portal template
        # For instance as defined in navigation.html: {% pluginblock "NavigationAdminPlugin" sand %}
        # This plugin is placed in the admin navigation bar.
        self.name = "NavigationAdminPlugin"
        # Define a GUID for each plugin.
        # Use e.g. http://www.guidgenerator.com/
        self.plugin_guid = "replace-with-guid"
        log.debug("Initiated MyNavBarPlugin")

    def return_string(self, tagname, *args):
        try:
            # Get the given theme
            theme = args[0][2]
        except:
            # fallback to sand theme
            theme = 'sand'
        return {'guid':self.plugin_guid, 'template':'%s/templates/plugins/PortalPluginTemplate/navigation_admin.html' % theme}

pluginblock = MyNavBarPlugin() 
