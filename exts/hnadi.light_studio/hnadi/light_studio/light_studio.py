from typing import List
from .light_profile import LightProfile
import omni.ui as ui
import omni.usd
import omni.kit.commands


class LightStuio():
    def __init__(self):
        self.CONTROLPANEL = False
        self._profiles: List[LightProfile] = []
        self.profileid = 0
        self.temp_profile = None

    def _add_proflie(self, profile_frame):
        profile = LightProfile(self)
        self._profiles.append(profile)
        self.profileid += 1
        self.run()
        self._build_profiles_ui(profile_frame)

    def _add_light(self, light_frame):
        self.selected_profile()._add_light(light_frame)

    def show(self):
        self.selected_profile().show()

    def run(self):
        for profile in self._profiles:
            profile.run()

    def destroy(self, profile_frame):
        for profile in self._profiles:
            profile.destroy(profile_frame)
        self.__init__()

    def _build_profiles_ui(self, profile_frame):
        with profile_frame:
            with ui.VStack(height=0):
                for i in range(0, len(self._profiles)):
                    path = self._profiles[i].path
                    button = ui.Button(path)
                    button.set_clicked_fn(lambda path=button.text: self.select_profile(path))

    def _clear(self, frame):
        with frame:
            with ui.VStack(height=0):
                ui.Spacer(height=0)

    def select_profile(self, path):
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

    def selected_profile(self):
        select_path = omni.usd.get_context().get_selection().get_selected_prim_paths()
        for i in range(0, len(self._profiles)):
            if select_path[0] == self._profiles[i].path:
                self.temp_profile = self._profiles[i]
        return self.temp_profile

    def selected_light(self):
        select_path = omni.usd.get_context().get_selection().get_selected_prim_paths()
        for i in range(0, len(self._profiles)):
            for j in range(0, len(self._profiles[i]._lights)):
                if select_path[0] == self._profiles[i]._lights[j].path:
                    return self._profiles[i]._lights[j]
