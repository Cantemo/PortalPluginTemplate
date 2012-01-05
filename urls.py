"""
URLS for the PortalPluginTemplate plugin
"""

from django.conf.urls.defaults import *

urlpatterns = patterns('portal.plugins.PortalPluginTemplate',
    # The URL defined to a hello world
    url(r'^helloworld/$', 'vmyplugin.HelloWorldView', name='my_plugin_helloworld', kwargs={'template':'hello_world.html'}),
    # The model and form views
    url(r'^modelsandforms/$', 'vmyplugin.MyPluginModelsView', name='my_plugin_models', kwargs={'template':'my_plugin_models_view.html'}),
    url(r'^modelsandforms/add/$', 'vmyplugin.MyPluginModelAddView', name='add_my_plugin_model', kwargs={'template':'my_plugin_model_view.html'}),
    url(r'^modelsandforms/delete/$', 'vmyplugin.MyPluginModelDeleteView', name='delete_my_plugin_model', kwargs={'template':'admin/confirm_delete.html'}),
    url(r'^modelsandforms/(?P<slug>[-\w\s]+)/$', 'vmyplugin.MyPluginModelAddView', name='my_plugin_model', kwargs={'template':'my_plugin_model_view.html'}),
    # MAM backend integration
    url(r'^mambackend/$', 'vmyplugin.MAMBackendInfoView', name='mam_backend_view', kwargs={'template':'mam_backend_view.html'}),

)
