# from .utils import get_icon_path
import omni.ui as ui
import omni.usd
from pxr import Gf, Sdf, UsdLux
import omni.kit.commands

import math


class LightCard:
    DSTANTLIGHT = "DistantLight"
    SPHERELIGHT = "SphereLight"
    RECTLIGHT = "RectLight"
    DISKLIGHT = "DiskLight"
    CYLINDERLIGHT = "CylinderLight"
    DOMELIGHT = "DomeLight"

    r = 500

    def __init__(
        self,
        profile
    ):
        self.SIZE = 30
        self.placer = ui.Placer(draggable=True, offset_x=ui.Percent(50), offset_y=ui.Percent(50))
        self.px = self.placer.offset_x
        self.py = self.placer.offset_y
        self._scale_x = 1.0
        self._scale_y = 1.0

        self._type = self.RECTLIGHT
        self.id = profile.lightid
        self.path = profile.path + '/' + self._type + '_' + str(self.id)

        self._buildprim = False
        self.intensity = 5000
        self.color_r = 0.75
        self.color_g = 0.75
        self.color_b = 0.75

        self.__profile = profile

    def _get_type(self, prim):
        if prim.IsA(UsdLux.DomeLight):
            return self.DOMELIGHT
        elif prim.IsA(UsdLux.DiskLight):
            return self.DISKLIGHT
        elif prim.IsA(UsdLux.RectLight):
            return self.RECTLIGHT
        elif prim.IsA(UsdLux.SphereLight):
            return self.SPHERELIGHT
        elif prim.IsA(UsdLux.CylinderLight):
            return self.CYLINDERLIGHT
        elif prim.IsA(UsdLux.DistantLight):
            return self.DSTANTLIGHT

    def _build_ui(self):
        self.placer = ui.Placer(draggable=True, offset_x=ui.Percent(self.px), offset_y=ui.Percent(self.py))
        with self.placer:
            ui.Rectangle(width=self.SIZE, height=self.SIZE, style={"background_color": 0xFFFFFFFF})

            def clamp_x(offset):
                if offset.value < 0:
                    self.placer.offset_x = ui.Percent(0)
                max_per = 100.0 - self.SIZE / self.placer.computed_width * 100.0
                if offset.value > max_per:
                    self.placer.offset_x = ui.Percent(max_per)
                self._scale_x = 1.0 - self.SIZE / self.placer.computed_width
                self.transform()

            def clamp_y(offset):
                if offset.value < 0:
                    self.placer.offset_y = ui.Percent(0)
                max_per = 100.0 - self.SIZE / self.placer.computed_height * 100.0
                if offset.value > max_per:
                    self.placer.offset_y = ui.Percent(max_per)
                self._scale_y = 1.0 - self.SIZE / self.placer.computed_height
                self.transform()

            # Calbacks
            self.placer.set_offset_x_changed_fn(clamp_x)
            self.placer.set_offset_y_changed_fn(clamp_y)

    def _build_prim(self):
        if self._buildprim is False:
            omni.kit.commands.execute(
                'CreatePrim',
                prim_type=self._type,
                attributes={'width': 100, 'height': 100, 'intensity': self.intensity})

            # Move path to the profile
            omni.kit.commands.execute(
                'MovePrim',
                path_from=omni.usd.get_context().get_selection().get_selected_prim_paths()[0],
                path_to=self.path)
            self._buildprim = True

    def transform(self):
        self.px = self.placer.offset_x / self._scale_x
        self.py = self.placer.offset_y / self._scale_y

        # Up ground
        # theta = (self.px-50)*1.8-90
        # phi = (self.py-50)*1.8-90

        # Global
        theta = (self.px-50)*3.6
        phi = (self.py-50)*3.6

        x = self.r * math.sin(theta * math.pi / 180) * math.cos(phi * math.pi / 180)
        y = self.r * math.sin(theta * math.pi / 180) * math.sin(phi * math.pi / 180)
        z = self.r * math.cos(theta * math.pi / 180)

        omni.kit.commands.execute(
            'TransformPrimSRT',
            path=Sdf.Path(self.path),
            new_translation=Gf.Vec3d(x, y, z),
            new_rotation_euler=Gf.Vec3d(0, theta, phi)
            )

    def destroy(self):
        omni.kit.commands.execute('DeletePrims', paths=[self.path])
        self.__profile._lights.remove(self)

    def _set_radius(self, radius):
        self.r = radius
        self.transform()

    def _set_intensity(self, intensity):
        omni.kit.commands.execute(
            'ChangeProperty',
            prop_path=Sdf.Path(self.path + '.intensity'),
            value=intensity,
            prev=self.intensity)

    def _set_color(self, r, g, b):
        omni.kit.commands.execute(
            'ChangeProperty',
            prop_path=Sdf.Path(self.path + '.color'),
            value=Gf.Vec3f(r, g, b),
            prev=self.color)
        self.color_r = r
        self.color_g = g
        self.color_b = b

    def _set_color_r(self, r):
        omni.kit.commands.execute(
            'ChangeProperty',
            prop_path=Sdf.Path(self.path + '.color'),
            value=Gf.Vec3f(r, self.color_g, self.color_b),
            prev=Gf.Vec3f(self.color_r, self.color_g, self.color_b))
        self.color_r = r

    def _set_color_g(self, g):
        omni.kit.commands.execute(
            'ChangeProperty',
            prop_path=Sdf.Path(self.path + '.color'),
            value=Gf.Vec3f(self.color_r, g, self.color_b),
            prev=Gf.Vec3f(self.color_r, self.color_g, self.color_b))
        self.color_g = g

    def _set_color_b(self, b):
        omni.kit.commands.execute(
            'ChangeProperty',
            prop_path=Sdf.Path(self.path + '.color'),
            value=Gf.Vec3f(self.color_r, self.color_g, b),
            prev=Gf.Vec3f(self.color_r, self.color_g, self.color_b))
        self.color_b = b
