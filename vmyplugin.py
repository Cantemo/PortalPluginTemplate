from portal.generic.baseviews import ClassView
from django.utils.translation import ugettext as _
from django.contrib import messages

import logging
from .models import MyPluginModel
from django.shortcuts import get_object_or_404
from .forms import MyPluginForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from portal.vidispine.iuser import UserHelper
from portal.vidispine.igeneral import performVSAPICall
log = logging.getLogger(__name__)


class HelloWorldView(ClassView):
    """
    Shows all the format rules
    """
    def __call__(self):
                
        extra_context = {'plugin_message':_("Hello World")}
        messages.success(self.request, message=_("Hello World message successfully sent"))
        log.debug("Hello World message successfully sent")
        return self.main(self.request, self.template, extra_context)


class MyPluginModelsView(ClassView):
    """ View all MyPluginModels
    """
    def __call__(self):
        _objs = MyPluginModel.objects.all()
        ctx = {"objects":_objs}
        return self.main(self.request, self.template, ctx)


class MyPluginModelView(ClassView):
    """ View a particular MyPluginModel
    """
    def __call__(self):
        self.slug = self.kwargs.get('slug')
        _obj = get_object_or_404(MyPluginModel, pk=self.slug)
        if self.request.method == 'POST':
            # Update an existing share rule
            _form = MyPluginForm(self.request.POST, instance=_obj)
            if _form.is_valid():
                log.debug("%s updating MyPluginModel %s" % (self.request.user, _obj.name))
                msr = _form.save()

                messages.success(self.request, _("Updated My Plugin Model"))
                return HttpResponseRedirect(reverse('my_plugin_models'))
        else:
            _form = MyPluginForm(instance=_obj)
            log.debug("%s viewing MyPluginModel %s" % (self.request.user, _obj.name))

        ctx = {"object":_obj, "form":_form}
        return self.main(self.request, self.template, ctx)


class MyPluginModelDeleteView(ClassView):
    """ Delete a particular MyPluginModel
    """
    def __call__(self):
        if self.request.method == 'POST':
            _deletable_objects = self.request.POST.getlist('selected_objects')
            for _d_o in _deletable_objects:
                _obj = MyPluginModel.objects.get(pk=_d_o)
                log.debug("%s deleted MyPluginModel %s" % (self.request.user, _obj.name))
                _obj.delete()
                _obj = None
            messages.success(self.request, _("Deleted My Plugin Model"))
            return HttpResponseRedirect(reverse('my_plugin_models'))
            
        else:
            log.debug("%s about to delete MyPluginModel" % self.request.user)
            _deletable_objects = self.request.GET.getlist('selected_objects')
            
            if len(_deletable_objects) < 1:
                messages.error(self.request, _("Please pick a My Plugin Model to delete"))
                return HttpResponseRedirect(reverse('my_plugin_models'))
            
            objects = []
            for (counter, i) in enumerate(_deletable_objects):
                try:
                    objects.append(MyPluginModel.objects.get(pk=i))
                except MyPluginModel.DoesNotExist:
                    messages.error(self.request, _("Tried to delete a My Plugin Model which didn't exist"))
                    return HttpResponseRedirect(reverse('my_plugin_models'))

        ctx = { "deletable_objects": _deletable_objects, "object_name": _("My Plugin Model"), "objects":objects}
        return self.main(self.request, self.template, ctx)


class MyPluginModelAddView(ClassView):
    """ Add a MyPluginModel
    """
    def __call__(self):
        if self.request.method == 'POST':
            _form = MyPluginForm(self.request.POST)
            
            # See if the form is valid 
            if _form.is_valid():
                log.debug("%s adding My Plugin Model" % self.request.user)
                msr = _form.save()
                return HttpResponseRedirect(reverse('my_plugin_models'))
        else:
            _form = MyPluginForm()

        ctx = {"form":_form}
        return self.main(self.request, self.template, ctx)


class MAMBackendInfoView(ClassView):
    """ View info from MAM backend
    """
    def __call__(self):
        if self.request.method == 'GET':
            uh = UserHelper(runas=self.request.user)
            # Get all users that are visible to the logged in user
            # This uses built-in functions in Portal.
            # performVSAPICall to properly make the API call and return any potentiel exceptions
            # UserHelper which is a helper class for interating with users in Vidispine
            res = performVSAPICall(func=uh.getAllUsers, args={'includeSelf':True, 'includeDisabled':True}, 
                                   vsapierror_templateorcode=None)
            if not res['success']:
                log.warning('Failed getting all users, error: %s' % res['exception']['error'])
                _users = []
            else:
                _users = res['response']

            ctx = {"users":_users}
            return self.main(self.request, self.template, ctx)
