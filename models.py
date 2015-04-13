from django.db import models
from django.utils.translation import ugettext as _
from vmysignallisteners import LastVisitedItems, PreMetadataUpdate

# Load and register LastVisitedItems
lastVisitedItems = LastVisitedItems()
lastVisitedItems.register()

# Load and register PreMetadataUpdate
preMetadataUpdate = PreMetadataUpdate()
preMetadataUpdate.register()

'''
Define your plugin model here.
More info: https://docs.djangoproject.com/en/dev/topics/db/models/

In order to create the database tables for this model, make sure that this
plugin is included in the APPS_TO_INSTALL list in settings.py.
Example: 
APPS_TO_INSTALL = [ ..., 'portal.plugins.PortalPluginTemplate', ... ]

Don't forget to do a 'python manage.py syncdb' afterwards!
'''
class MyPluginModel(models.Model):
    """ Definition of a plugin model.
        
    """
    name = models.CharField(_("Name"), max_length=255, blank=False, null=False)
    description = models.TextField(_("Description"), blank=True, null=True)
    external_id = models.CharField(_("External ID"), max_length=64, blank=False, null=False)
    
    class Meta:
        verbose_name = _("My Plugin Model")
        verbose_name_plural = _("My Plugin Model")

    def __unicode__(self):
        _name= self.name + " (" + self.external_id + ")"
        return _name
    
