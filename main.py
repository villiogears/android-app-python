from kivy.app import App
from kivy.clock import Clock
from kivy.uix.stacklayout import StackLayout
from kivy.uix.image import Image
from kivy.utils import platform
try:
    if platform == 'android':
        from jnius import autoclass, cast
        from android import activity
    else:
        autoclass = cast = activity = None
except ImportError:
    autoclass = cast = activity = None
from functools import partial
from datetime import datetime
from os.path import exists


