"""
An example and test plugin for Item Page, SubClip Page, Sharing Page and Annotation Tool video player option overrides.

These plugins are supported in Portal 3.4.5 and later.

Some of these examples are available in documentation as well.
"""

from portal.generic.plugin_interfaces import IPluginBlock
from portal.pluginbase.core import Plugin, implements


class ItemPageCustomSubtitlesPlugin(Plugin):
    """
    Add a (hard coded) custom subtitle source to Item page video player.
    """
    implements(IPluginBlock)

    def __init__(self):
        self.name = "MediaViewVideoPlayerOptionsJS"
        self.plugin_guid = 'bf729d14-caa1-4978-96c8-0927361bcb07'

    def return_string(self, tagname, *args):
        # For simplicity: Return JavaScript defined directly in this source file.
        # Best practice is to use a separate template file.
        javascript_code = """
            // ItemPageCustomSubtitlesPlugin: Override subtitles with a hardcoded custom WEBVTT source
            // Item page playerOptions always has a timeline with one object.
            playerOptions.timeline[0].textTracks = [
                {
                    code: "de",
                    kind: "subtitles",
                    name: gettext("German"),
                    // This URL must point to an endpoint that returns WEBVTT formatted subtitles, e.g. the
                    // following assumes item VX-4 has shape VX-6 that is a .webvtt file for current media item.
                    url: "/vs/item/download/VX-4/?shape=VX-6"
                },
                {
                    name: gettext("Disabled")
                }
            ];
        """

        return {'guid': self.plugin_guid, 'string': javascript_code}


ItemPageCustomSubtitlesPlugin()


class ItemPageDisableSubtitlesPlugin(Plugin):
    """
    Example: Disable subtitles from item page.
    """
    implements(IPluginBlock)

    def __init__(self):
        self.name = "MediaViewVideoPlayerOptionsJS"
        self.plugin_guid = 'dbee3017-a8ff-4b90-bbb2-e9f77f0e12e6'

    def return_string(self, tagname, *args):
        # For simplicity: Return JavaScript defined directly in this source file.
        # Best practice is to use a separate template file.
        javascript_code = """
            // ItemPageCustomSubtitlesPlugin: Disable textTracks from player
            playerOptions.timeline[0].textTracks = null;
        """

        return {'guid': self.plugin_guid, 'string': javascript_code}


# Commented out since this and ItemPageCustomSubtitlesPlugin should not be enabled at the same time.
# If you enable this, please comment our initialization ItemPageCustomSubtitlesPlugin()
# ItemPageDisableSubtitlesPlugin()


class ItemPageDisableCreatePoster(Plugin):
    """
    Override player options to disable poster image creation with "camera" button.
    """
    implements(IPluginBlock)

    def __init__(self):
        self.name = "MediaViewVideoPlayerOptionsJS"
        self.plugin_guid = '8c7eb227-c0c4-42ad-83b9-257569fe11fc'

    def return_string(self, tagname, *args):
        # For simplicity: Return JavaScript defined directly in this source file.
        # Best practice is to use a separate template file.
        javascript_code = """
            // ItemPageDisableCreatePoster: Disable poster creation from video player
            playerOptions.grabStills = false;
        """

        return {'guid': self.plugin_guid, 'string': javascript_code}


ItemPageDisableCreatePoster()


class AnnotationToolCustomSubtitles(Plugin):
    """
    Override player options in Annotation Tool to add custom subtitles.
    """
    implements(IPluginBlock)

    def __init__(self):
        self.name = "AnnotationViewJS"
        self.plugin_guid = '66fcdc0c-b89d-4c4a-8578-04a8d829ae0f'

    def return_string(self, tagname, *args):
        # For simplicity: Return JavaScript defined directly in this source file.
        # Best practice is to use a separate template file.
        javascript_code = """
            <script>
                $(document).ready(function() {
                    cntmo.app.annotationTool.playerOptionHandler = function(playerOptions) {
                        // Set custom textTrack data with a single subtitle source on by default, secondary option
                        // disabled. In Annotation Tool, playerOptions.timeline always has one object.
                        playerOptions.timeline[0].textTracks = [
                            {
                                code: "de",
                                kind: "subtitles",
                                name: gettext("German"),
                                // This URL must point to an endpoint that returns WEBVTT formatted subtitles, e.g. the
                                // following assumes item VX-4 / shape VX-6 is a .webvtt file for current media item.
                                url: "/vs/item/download/VX-4/?shape=VX-6"
                            },
                            {
                                name: gettext("Disabled")
                            }
                        ];
                        return playerOptions;
                    }
                });
            </script>
        """

        return {'guid': self.plugin_guid, 'string': javascript_code}


AnnotationToolCustomSubtitles()
