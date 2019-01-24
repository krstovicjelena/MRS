from plugin_framework.plugin import Plugin
from .widgets.placevi_list import PlaceviWidget

class Main(Plugin):

    def __init__(self, spec):

        super().__init__(spec)

    def get_widget(self, parent=None):
        return PlaceviWidget(parent), None, None
