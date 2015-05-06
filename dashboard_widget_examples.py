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


class RSSFeedWidget(Plugin):
    """
    A Dashboard widget for following an RSS feed.

    Warning: For simplicity this example widget does not use ETag or Last-Modified headers to reduce bandwidth.
    This means that for each update by each user the RSS feed is fully reloaded. With a frequent refresh interval
    the publisher may ban you from accessing their server, usually temporarily.
    """
    implements(IDashboardWidget)

    default_refresh = 30  # seconds
    default_feeds = (
        ('http://feeds.reuters.com/reuters/USVideoBreakingviews', "Reuters Breakingviews Video"),
        ('http://rss.cnn.com/rss/edition.rss', "CNN Top Stories"),
        ('http://rss.cnn.com/rss/cnn_latest.rss', "CNN Most Recent"),
        ('http://lorem-rss.herokuapp.com/feed?unit=second&interval=30', "Lorem Ipsum 30 sec"),
        ('http://lorem-rss.herokuapp.com/feed?unit=second&interval=5', "Lorem Ipsum 5 sec"),
        ('http://lorem-rss.herokuapp.com/feed?unit=second&interval=1', "Lorem Ipsum 1 sec"),
    )

    default_entry_count = 10

    _cache_timeout = 3600  # seconds

    def __init__(self):
        self.name = 'RSSFeedWidget'
        self.plugin_guid = '19F4BB8E-343D-43A6-A2A6-AC16D66CEA73'
        self.template_name = 'rss_feed_widget.html'
        self.configurable = True

    @staticmethod
    def get_list_title():
        return _("RSS feed")

    @staticmethod
    def _get_feed_cache_key(widget_id, session_key):
        """
        Get cache key for feed instance data.

        Previous entries are stored into cache to be able to animate new and old entries. If cache is disabled
        the widget will still work, but will not animate changes correctly.
        """
        return "RSSFeedWidget:%s:%s" % (widget_id, session_key)

    @staticmethod
    def get_render_data(render_data, settings, request):
        # Note: Django cache must be imported inside method:
        from django.core.cache import cache
        from time import time

        # Pass refresh interval to template
        try:
            render_data['refresh_interval'] = settings['refresh_interval']
        except KeyError:
            render_data['refresh_interval'] = RSSFeedWidget.default_refresh

        # Get feed_url from widget instance settings
        try:
            if settings['feed_url'] == 'custom':
                feed_url = settings['custom_url']
            else:
                feed_url = settings['feed_url']
        except KeyError:
            # settings is not initialized at all, use default feed
            feed_url = RSSFeedWidget.default_feeds[0][0]

        # Pass feed_url to template, potentially shown in error message
        render_data['feed_url'] = feed_url

        try:
            import feedparser
        except ImportError:
            render_data['error'] = (
                "Could not import \"feedparser\" library, install it with the following "
                "command and restart Portal:"
                "\n\n\n$ /opt/cantemo/python/bin/pip install feedparser"
            )
            return render_data

        # Read and parse the feed from the URL. Note: This always reads the full feed.
        start_time = time()
        parsed = feedparser.parse(feed_url)
        log.debug('RSSFeedWidget, feed loaded in %i ms, feed_url: %s', (time() - start_time) * 1000, feed_url)
        if parsed.bozo:
            log.error('Error parsing feed: %s', parsed.bozo_exception)
            render_data['error'] = repr(parsed.bozo_exception)
        else:
            # Current feed is passed to template
            render_data['feed'] = parsed.feed
            # Widget title is updated based on feed title
            render_data['title'] += ': ' + parsed.feed.title

            def entry_hash(e):
                # Entries are compared by the results of this function, so e.g. e.is_new does not affect comparison
                return e.published + e.title

            # Combine the new and previous entries into one list, marking which entries are new, and which should
            # be removed
            cache_key = RSSFeedWidget._get_feed_cache_key(render_data['id'], request.session.session_key)
            previous_entries = cache.get(cache_key, [])
            # Always limit entries to entry_count/default_entry_count
            try:
                entry_count = settings['entry_count']
            except KeyError:
                entry_count = RSSFeedWidget.default_entry_count
            parsed_entries = parsed.entries[:entry_count]
            cache.set(cache_key, parsed_entries, RSSFeedWidget._cache_timeout)

            previous_set = set(entry_hash(e) for e in previous_entries)
            parsed_set = set(entry_hash(e) for e in parsed_entries)

            render_entries = list(previous_entries)
            for e in render_entries:
                if not entry_hash(e) in parsed_set:
                    e.to_remove = True
                else:
                    e.to_remove = False
                e.is_new = False
            insert_to = 0
            for e in parsed_entries:
                if not entry_hash(e) in previous_set:
                    render_entries.insert(insert_to, e)
                    e.is_new = True
                    e.to_remove = False
                    insert_to += 1
            render_data['entries'] = render_entries

        return render_data

    @staticmethod
    def force_show_config(settings, request):
        # Show configuration if feed URL has not been set
        return 'feed_url' not in settings

    @staticmethod
    def get_config_form(settings, request):
        from django import forms

        class RSSFeedWidgetSettings(forms.Form):
            choices = RSSFeedWidget.default_feeds + (('custom', _("Custom RSS URL")),)
            feed_url = forms.ChoiceField(label=_("Feed to display"), choices=choices)
            custom_url = forms.URLField(label=_("Custom RSS URL"), required=False)
            refresh_interval = forms.IntegerField(label=_('Refresh interval (seconds):'),
                                                  initial=RSSFeedWidget.default_refresh, min_value=1)
            entry_count = forms.IntegerField(label=_('How many entries to show:'),
                                             initial=RSSFeedWidget.default_entry_count, min_value=1)

        return RSSFeedWidgetSettings

# Registers this class to global plugins
RSSFeedWidget()
