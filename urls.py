"""
URLS for the PortalPluginTemplate plugin
"""

from django.urls import re_path
from .vmyplugin import (HelloWorldView, MyPluginModelsView, MyPluginModelAddView,
                        MyPluginModelDeleteView, MyPluginModelView, MAMBackendInfoView)

urlpatterns = [
    # The URL defined to a hello world
    re_path(r'^helloworld/$', HelloWorldView, name='my_plugin_helloworld',
        kwargs={'template': 'portalplugintemplate/hello_world.html'}),
    # The model and form views
    re_path(r'^modelsandforms/$', MyPluginModelsView, name='my_plugin_models',
        kwargs={'template': 'portalplugintemplate/my_plugin_models_view.html'}),
    re_path(r'^modelsandforms/add/$', MyPluginModelAddView, name='add_my_plugin_model',
        kwargs={'template': 'portalplugintemplate/my_plugin_model_view.html'}),
    re_path(r'^modelsandforms/delete/$', MyPluginModelDeleteView, name='delete_my_plugin_model',
        kwargs={'template': 'admin/confirm_delete.html'}),
    re_path(r'^modelsandforms/(?P<slug>[-\w\s]+)/$', MyPluginModelView, name='my_plugin_model',
        kwargs={'template': 'portalplugintemplate/my_plugin_model_view.html'}),
    # MAM backend integration
    re_path(r'^mambackend/$',  MAMBackendInfoView, name='mam_backend_view',
        kwargs={'template': 'portalplugintemplate/mam_backend_view.html'}),
]
