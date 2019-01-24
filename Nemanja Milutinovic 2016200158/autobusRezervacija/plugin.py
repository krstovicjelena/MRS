from plugin_framework.plugin import Plugin
from .widgets.autobus_list import AutobusWidget

class Main(Plugin):

    def __init__(self, spec):

        super().__init__(spec)

    def get_widget(self, parent=None):
        return AutobusWidget(parent), None, None
