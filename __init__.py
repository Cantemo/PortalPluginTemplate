'''
Import all plugins here
'''
from plugin import *
try:
    from dashboard_widget_examples import *
except ImportError:
    # This only works on portal 2.1 or later
    pass

try:
    from video_player_options import *
except ImportError:
    # This only works on portal 3.4.5 or later
    pass

__version__ = "DEVEL"
