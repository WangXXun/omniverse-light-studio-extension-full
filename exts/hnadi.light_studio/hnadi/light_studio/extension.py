from .window import LightStudioWindow
import omni.ext
import omni.kit.commands
from omni.kit.widgets.custom import WindowExtension

import carb.input


# NVIDIA COLOR: 0xFF00B976
NVIDIACOLOR = 0xFF00B976
EXTENSION_MENU_PATH = "Window/LightStudio"


# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.
class LightStudioExtension(omni.ext.IExt, WindowExtension):
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.

    def on_startup(self, ext_id):
        WindowExtension.on_startup(
            self, menu_path="Light Studio",
            hotkey=(carb.input.KEYBOARD_MODIFIER_FLAG_CONTROL, carb.input.KeyboardInput.L)
        )

    def on_shutdown(self):
        WindowExtension.on_shutdown(self)

    def _create_window(self):
        self._window = LightStudioWindow()
        return self._window
