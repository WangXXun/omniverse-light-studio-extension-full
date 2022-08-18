from .light_studio import LightStuio
import omni.ui as ui
from omni.kit.widgets.custom import SimpleImageButton

from .utils import get_icon_path, set_mode


class LightStudioWindow(ui.Window):

    studio = LightStuio()

    def __init__(self):
        super().__init__("Light Studio", width=300, height=610)

        self.frame.set_build_fn(self._build_ui)
        self.deferred_dock_in("Property", ui.DockPolicy.CURRENT_WINDOW_IS_ACTIVE)

    def destroy(self):
        super().destroy()

    def _build_ui(self):
        self._build_content()

    def _build_content(self):
        with self.frame:
            with ui.VStack(
                style={
                    "Label: hovered": {"color": 0xF},
                    "Button": {"background_color": 0xF}
                },
                height=0
            ):
                self.Studio()
                self.Profiles()
                self.Lights()
                self.Property()

                ui.Label("Light studio extension ©HNADI", height=30)

    def Studio(self):
        ui.Spacer(height=10)
        with ui.HStack():
            ui.Spacer(width=ui.Percent(30))
            self.ControlPanelButton = SimpleImageButton(
                get_icon_path("Off.png"),
                50,
                clicked_fn=lambda: self.ControlPanel_Set())
            ui.Spacer(width=ui.Percent(15))
            self.update_button = SimpleImageButton(
                get_icon_path("Update.png"),
                50,
                clicked_fn=lambda: self.ControlPanel_On())
        ui.Spacer(height=10)

    def Profiles(self):
        with ui.CollapsableFrame("Profile"):
            with ui.HStack(spacing=10):
                # Lights profiles
                with ui.VStack():
                    self.profile_frame = ui.ScrollingFrame(
                        height=90,
                        horizontal_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_ALWAYS_OFF,
                        vertical_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_ALWAYS_ON,)
                    self.studio._build_profiles_ui(self.profile_frame)

                with ui.VStack(width=30):
                    add_profile = ui.Button("", tooltip="Add", image_url=get_icon_path("plus.png"))
                    add_profile.set_clicked_fn(lambda: self.studio._add_proflie(self.profile_frame))

                    delete_profile = ui.Button("", tooltip="Delete", image_url=get_icon_path("minus.png"))
                    delete_profile.set_clicked_fn(lambda: self.studio.selected_profile().destroy(self.profile_frame))
                    clear_profile = ui.Button("", tooltip="Clear", image_url=get_icon_path("Clear.png"))
                    clear_profile.set_clicked_fn(
                        lambda: self.studio._clear(self.profile_frame))

    def Lights(self):
        with ui.CollapsableFrame("Lights"):
            with ui.HStack(spacing=10):
                # Lights list
                with ui.VStack():
                    self.light_frame = ui.ScrollingFrame(
                        height=90,
                        horizontal_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_ALWAYS_OFF,
                        vertical_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_ALWAYS_ON,)
                    if self.studio.selected_profile() is not None:
                        self.studio.selected_profile()._build_lights_ui(self.light_frame)

                # Lights controller
                with ui.VStack(width=30):
                    add_light = ui.Button("", tooltip="Add", image_url=get_icon_path("plus.png"))
                    add_light.set_clicked_fn(lambda: self.studio._add_light(self.light_frame))

                    delete_light = ui.Button("", tooltip="Delete", image_url=get_icon_path("minus.png"))
                    delete_light.set_clicked_fn(lambda: self.studio.selected_light().destroy())
                    clear_light = ui.Button("", tooltip="Clear", image_url=get_icon_path("Clear.png"))
                    clear_light.set_clicked_fn(
                        lambda: self.studio._clear(self.light_frame))

    # This part can quickly adjust the light properties,
    # but at this stage I recommend using the light property widget
    def Property(self):
        with ui.CollapsableFrame("Selected Light"):
            with ui.VStack(spacing=5, height=120):
                ui.Spacer(height=5)
                # ui.Label("This part can quickly adjust the light properties,")
                # ui.Label("but at this stage I recommend using the light property widget.")

                # Set color
                with ui.HStack():
                    ui.Label("Color Overlay:", width=100)
                    with ui.HStack(spacing=5):
                        color_model = ui.ColorWidget(0.75, 0.75, 0.75, width=0, height=0).model

                        r_model = color_model.get_item_children()[0]
                        r_component = color_model.get_item_value_model(r_model)
                        ui.FloatDrag(r_component, min=0, max=1)
                        r_component.add_value_changed_fn(
                            lambda r: self.studio.selected_light()._set_color_r(r.get_value_as_float()))

                        g_model = color_model.get_item_children()[1]
                        g_component = color_model.get_item_value_model(g_model)
                        ui.FloatDrag(g_component, min=0, max=1)
                        g_component.add_value_changed_fn(
                            lambda g: self.studio.selected_light()._set_color_g(g.get_value_as_float()))

                        b_model = color_model.get_item_children()[2]
                        b_component = color_model.get_item_value_model(b_model)
                        ui.FloatDrag(b_component, min=0, max=1)
                        b_component.add_value_changed_fn(
                            lambda b: self.studio.selected_light()._set_color_b(b.get_value_as_float()))

                # Set type of selected light
                with ui.HStack():
                    ui.Label("Type:", width=100)
                    options = (
                        2,
                        "Distant Light",
                        "Sphere Light",
                        "Rect Light",
                        "Disk Light",
                        "Cylinder Light",
                        "Dome Light"
                    )
                    ui.ComboBox(*options)

                # Set distance of selected light
                with ui.HStack():
                    ui.Label("Distance:", width=100)
                    radius = ui.FloatDrag(
                        min=0,
                        step=1,
                        style={
                            "border_radius": 5,
                            "background_color": 0xFF111111
                        }).model
                    radius.set_value(500)
                    radius.add_value_changed_fn(
                        lambda x: self.studio.selected_light()._set_radius(x.get_value_as_float()))

                # Set intensity of selected light
                with ui.HStack():
                    ui.Label("Intensity:", width=100)
                    intensity = ui.IntDrag(
                        min=0,
                        step=10,
                        style={
                            "border_radius": 5,
                            "background_color": 0xFF111111
                        }).model
                    intensity.set_value(5000)
                    intensity.add_value_changed_fn(
                        lambda x: self.studio.selected_light()._set_intensity(x.get_value_as_int()))

    def ControlPanel_Set(self):
        if self.studio.CONTROLPANEL is False:
            self.ControlPanel_On()
        else:
            self.ControlPanel_Off()

    def ControlPanel_On(self):
        set_mode()
        self.ControlPanelButton.set_image(get_icon_path("On.png"))
        self.studio.CONTROLPANEL = True

        self._windowControl = ui.Window("Control Panel", width=600, height=300)
        with self._windowControl.frame:
            with ui.ZStack():
                # Background
                ui.Rectangle(style={"background_color": 0xFF111111})
                self.studio.show()

    def ControlPanel_Off(self):
        self.ControlPanelButton.set_image(get_icon_path("Off.png"))
        self.studio.CONTROLPANEL = False

        self._windowControl.destroy()
        self.studio.destroy(self.profile_frame)

        with self._windowControl.frame:
            with ui.ZStack():
                ui.Rectangle(style={"background_color": 0xFF111111})
