from .light_card import LightCard
from pxr import UsdGeom
import omni.kit.commands
import omni.usd
import omni.ui as ui

from typing import List


class LightProfile:
    __INSTANCE__ = None

    def __init__(self, studio):
        self._base = UsdGeom.Xform()
        self._lights: List[LightCard] = []
        self.id = studio.profileid
        self.lightid = 0

        self.__studio = studio

        omni.kit.commands.execute(
            'CreatePrim',
            prim_type='Xform',
            attributes={})

        defaultpath = omni.usd.get_context().get_selection().get_selected_prim_paths()[0]
        self.path = defaultpath + '_' + str(self.id)
        omni.kit.commands.execute(
            'MovePrim',
            path_from=defaultpath,
            path_to=self.path)

    def _add_light(self, light_frame):
        light = LightCard(self)
        self._lights.append(light)
        self.lightid += 1
        self.show()
        self.run()
        self._build_lights_ui(light_frame)

    def show(self):
        for light in self._lights:
            light._build_ui()

    def run(self):
        for light in self._lights:
            light._build_prim()
            light.transform()

    def destroy(self, profile_frame):
        omni.kit.commands.execute('DeletePrims', paths=[self.path])
        self.__studio._profiles.remove(self)
        self.__studio._build_profiles_ui(profile_frame)

    def _build_lights_ui(self, light_frame):
        with light_frame:
            with ui.VStack(height=0):
                for i in range(0, len(self._lights)):
                    path = self._lights[i].path
                    button = ui.Button(path)
                    button.set_clicked_fn(lambda path=button.text: self.select_light(path))

    def select_light(self, path):
        select_path = omni.usd.get_context().get_selection().get_selected_prim_paths()
        if select_path is None:
            omni.kit.commands.execute(
                'SelectPrimsCommand',
                old_selected_paths=[],
                new_selected_paths=[path],
                expand_in_stage=True)
        else:
            omni.kit.commands.execute(
                'SelectPrims',
                old_selected_paths=[select_path],
                new_selected_paths=[path],
                expand_in_stage=True)
        print(path)
