"""
This module contains example dashboard widgets.
"""
import logging

from django.utils.translation import ugettext as _

from portal.pluginbase.core import Plugin, implements
from portal.generic.dashboard_interfaces import IDashboardWidget
# Note: The following package must be imported at call-time in methods to prevent circular dependencies:
# from django import forms
# from django.core.cache import cache

log = logging.getLogger(__name__)


class HelloWidget(Plugin):
    implements(IDashboardWidget)

    def __init__(self):
        self.name = 'HelloWidget'
        self.plugin_guid = '2BFADB52-56B8-47B3-BA63-1383CD42F678'
        self.template_name = IDashboardWidget.default_template
        self.configurable = False
        # Note: Since configurable is False, this class does not need to implement
        # force_show_config() and get_config_form()

    @staticmethod
    def get_list_title():
        return "Hello widget"

    @staticmethod
    def get_render_data(render_data, settings, request):
        render_data['content'] = "Hello world!"
        return render_data


HelloWidget()


class DummyWidget(Plugin):
    """
    A simple example widget with a custom template.

    Note: Since configurable is False, this class does not need to implement force_show_config() and get_config_form()
    """
    implements(IDashboardWidget)

    def __init__(self):
        self.name = 'DummyWidget'
        self.plugin_guid = '4DA92DF6-9579-4813-8BEF-525AE897D750'
        self.template_name = 'dummy_widget.html'
        self.configurable = False

    @staticmethod
    def get_list_title():
        return _("Dummy widget")

    @staticmethod
    def get_render_data(render_data, settings, request):
        return render_data

# This registers the widget plugin
DummyWidget()


class TextWidget(Plugin):
    """
    A basic widget with configurable text and title
    """
    implements(IDashboardWidget)

    def __init__(self):
        self.name = 'TextWidget'
        self.plugin_guid = 'DF194309-B4A0-4855-A362-D99E171044D9'
        self.template_name = IDashboardWidget.default_template
        self.configurable = True

    @staticmethod
    def get_list_title():
        return _("Text widget")

    @staticmethod
    def get_render_data(render_data, settings, request):
        # Update widget title from settings if user has edited the text
        if 'title' in settings:
            render_data['title'] = settings['title']
        if 'text' in settings:
            render_data['content'] = settings['text']
        else:
            render_data['content'] = _(
                "You can configure this text to by clicking the wrench in the upper right corner.")
        return render_data

    @staticmethod
    def get_config_form(settings, request):
        from django import forms

        class TextWidgetSettingsForm(forms.Form):
            title = forms.CharField(label='Widget title', max_length=100, initial=TextWidget.get_list_title())
            text = forms.CharField(label='Widget text', max_length=10000, widget=forms.Textarea(attrs={'rows': 5}))

        return TextWidgetSettingsForm

    @staticmethod
    def force_show_config(settings, request):
        return False

# This registers the widget plugin
TextWidget()


class TextWidgetForcedConfig(TextWidget):
    """
    A version of text widget that shows configuration screen by default, until user has entered a text.

    Subclass of TextWidget, overrides __init__(), get_list_title(), and force_show_config().
    """

    def __init__(self):
        TextWidget.__init__(self)
        self.name = 'TextWidgetForcedConfig'
        self.plugin_guid = 'A9F34DA4-7E75-4CD6-8CBC-FDD4973A2989'

    @staticmethod
    def get_list_title():
        return _("Text widget forced config")

    @staticmethod
    def force_show_config(settings, request):
        """
        Force this widget to edit mode if text has not yet been set, or is empty
        """
        return 'text' not in settings or not settings['text']


TextWidgetForcedConfig()


class RefreshWidget(Plugin):
    """
    Example of a widget that automatically refreshes every 10 seconds.

    Uses custom template which does JS reload using
    cntmo.app.dashboard.reloadWidgetAfter(id, time_ms)-function.
    """
    implements(IDashboardWidget)

    default_interval = 10

    def __init__(self):
        self.name = 'RefreshWidget'
        self.plugin_guid = '3622B952-E9C0-4429-BD00-65B6958322BF'
        self.template_name = 'refresh_widget.html'
        self.configurable = True

    @staticmethod
    def get_list_title():
        return _("Refresh widget")

    @staticmethod
    def get_render_data(render_data, settings, request):
        from datetime import datetime

        render_data['content'] = _("Time on server: {}").format(
            datetime.now().isoformat(' '))
        # Make sure refresh_interval is passed to template (use default
        # if user has not edited settings yet)
        if 'refresh_interval' in settings:
            render_data['refresh_interval'] = settings['refresh_interval']
        else:
            render_data['refresh_interval'] = RefreshWidget.default_interval
        return render_data

    @staticmethod
    def get_config_form(settings, request):
        # Django classes MUST be imported inside method, not when package
        # is initialized
        from django import forms

        class RefreshWidgetSettingsForm(forms.Form):
            refresh_interval = forms.IntegerField(
                label=_('Refresh interval (seconds):'),
                initial=RefreshWidget.default_interval, min_value=1)

        return RefreshWidgetSettingsForm

    @staticmethod
    def force_show_config(settings, request):
        return False

# Register widget plugin
RefreshWidget()


class ConfigTestWidget(Plugin):
    """
    Test widget for all types of supported configuration fields. When configuration is saved, shows all stored
    settings-values and their types.

    Note: Django fields DateField, MultipleChoiceField and DecimalField are NOT supported in widgets.
    """
    implements(IDashboardWidget)

    def __init__(self):
        self.name = 'ConfigTestWidget'
        self.plugin_guid = '31C1A0C7-3B26-44C3-9881-0D74314C9BF0'
        self.template_name = IDashboardWidget.default_template
        self.configurable = True

    @staticmethod
    def get_list_title():
        return _("Configuration test widget")

    @staticmethod
    def get_render_data(render_data, settings, request):
        content = 'All settings values:'
        for key, value in sorted(settings.iteritems()):
            content += '\n"%s": %r (%s)' % (key, value, type(value).__name__)
        content += '\nn=%s' % len(settings)
        render_data['content'] = content
        return render_data

    @staticmethod
    def get_config_form(settings, request):
        from django import forms

        choices = ((1, "first option"), (2, "second option"), (3, "third option"))

        class SettingsForm(forms.Form):
            boolean = forms.BooleanField(label='BooleanField', required=False)
            char = forms.CharField(label='CharField', required=False)
            choice = forms.ChoiceField(label='ChoiceField', choices=choices)
            email = forms.EmailField(label='EmailField', required=False)
            float = forms.FloatField(label='FloatField', required=False)
            integer = forms.IntegerField(label='IntegerField', initial=1)
            null_boolean = forms.NullBooleanField(label='NullBooleanField', required=False)
            url = forms.URLField(label='URLField', required=False)

        return SettingsForm

    @staticmethod
    def force_show_config(settings, request):
        return False


ConfigTestWidget()
