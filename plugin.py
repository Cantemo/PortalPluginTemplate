from portal.pluginbase.core import *
from portal.generic.plugin_interfaces import IPluginURL, IPluginBlock,\
    IContextProcessor, IAppRegister
from django.template import loader, Context

import logging
log = logging.getLogger(__name__)


class MyPluginURL(Plugin):
    """
    URL Plugin that defines new URL's in the system
    Loads the Admin rules URL's
    """
    implements(IPluginURL)
    
    def __init__(self):
        self.name = "MyPluginURL"
        # Should point to the urls.py
        self.urls = 'portal.plugins.PortalPluginTemplate.urls'
        # Defines the URL pattern prefix
        self.urlpattern = r'^myplugin/'
        # Defines the plugin namespace
        self.namespace = 'myplugin'
        # Define a GUID for each plugin.
        # Use e.g. http://www.guidgenerator.com/
        self.plugin_guid = "906ec22a-bfd4-48be-8d57-4cf8f4cb2da8"
        log.debug("Initiated MyPluginURL")


# Load the URL plugin
MyPluginURL()


class MyPluginAdminMenu(Plugin):
    """
    Adds the plugin to the admin menu
    """
    
    implements(IPluginBlock)

    def __init__(self):
        # The name of the plugin which should match the pluginblock tag in the Portal template
        # For instance as defined in base_admin.html: {% pluginblock "AdminLeftPanelBottomPanePlugin" sand %}
        # This plugin is placed in the Admin page, in the left panel at the bottom
        self.name = "AdminLeftPanelBottomPanePlugin"
        # Define a GUID for each plugin.
        # Use e.g. http://www.guidgenerator.com/
        self.plugin_guid = "2ada3ec1-6cb7-464f-b0f7-22ab19ff1527"
        log.debug("Initiated MyPluginBlock")

    def return_string(self, tagname, *args):
        try:
            # Get the given theme
            theme = args[0][2]
        except:
            # fallback to sand theme
            theme = 'sand'
        return {'guid': self.plugin_guid, 'template': 'portalplugintemplate/admin_leftpanel_entry.html'}


MyPluginAdminMenu()


class MyNavBarPlugin(Plugin):
    implements(IPluginBlock)

    def __init__(self):
        # The name of the plugin which should match the pluginblock tag in the Portal template
        # For instance as defined in navigation.html: {% pluginblock "NavigationAdminPlugin" sand %}
        # This plugin is placed in the admin navigation bar.
        self.name = "NavigationAdminPlugin"
        # Define a GUID for each plugin.
        # Use e.g. http://www.guidgenerator.com/
        self.plugin_guid = "2d700d00-7edc-445a-913f-e15686f7c9e2"
        log.debug("Initiated MyNavBarPlugin")

    def return_string(self, tagname, *args):
        try:
            # Get the given theme
            theme = args[0][2]
        except:
            # fallback to sand theme
            theme = 'sand'
        return {'guid': self.plugin_guid, 'template': 'portalplugintemplate/navigation_admin.html'}


MyNavBarPlugin()


class MyGearboxMenuPlugin(Plugin):
    implements(IPluginBlock)

    def __init__(self):
        # The name of the plugin which should match the pluginblock tag in the Portal template
        # For instance as defined in media_view.html: {% pluginblock "MediaViewDropdown" %}
        # This plugin is placed in the gearbox menu for the item.
        self.name = "MediaViewDropdown"
        # Define a GUID for each plugin.
        # Use e.g. http://www.guidgenerator.com/
        self.plugin_guid = "03eed808-5c6b-42a7-88a1-0336bcf790d1"
        log.debug("Initiated MyGearboxMenuPlugin")

    def return_string(self, tagname, *args):
        return {'guid': self.plugin_guid, 'template': 'portalplugintemplate/gearbox_menu.html'}


MyGearboxMenuPlugin()


class ItemContextPlugin(Plugin):
    implements(IContextProcessor) 
    
    def __init__(self):
        self.name = "ItemContextPlugin"
        # Define a GUID for each plugin.
        # Use e.g. http://www.guidgenerator.com/
        self.plugin_guid = "7d024a0e-47ea-45b7-93b9-ae115a8ee7fa"
        log.debug("Initiated ItemContextPlugin")
        
    def __call__(self,context, class_object):
        from portal.vidispine.vitem import ItemView
        if isinstance(class_object, ItemView) is False:
            return context

        self.context = context
        self.class_object = class_object 
        #self.username = "test" 
        return self.process_context()
    
    def process_context(self):
        extra_context = self.context.dicts[len(self.context.dicts)-1]
        # Do plugin stuff here and modify the extra_context
        # extra_context['my_new_data_key'] = 'my new data value' 

        return self.context


ItemContextPlugin()


class PortalPluginTemplatePluginRegister(Plugin):
    implements(IAppRegister)

    def __init__(self):
        self.name = "PortalPluginTemplateRegister"
        self.plugin_guid = "2b622e08-e442-44da-ac5b-cd73f3fc7e70"
        log.debug('Registered the PortalPluginTemplate App')

    def __call__(self):
        from .__init__ import __version__ as versionnumber
        _app_dict = {
            'name': 'PortalPluginTemplate Plugin',
            'version': versionnumber,
            'author': 'Cantemo AB',
            'author_url': 'www.cantemo.com',
            'notes': 'Copyright 2012-2015. All Rights Reserved'}
        return _app_dict


PortalPluginTemplatePluginRegister()
