from pathlib import Path
import carb
import omni.usd


def get_icon_path(icon_file):
    path = Path(__file__).parent
    count = 7
    while count > 0:
        if Path.exists(path.joinpath("data")):
            return path.joinpath(f"data/{icon_file}").as_posix()
        path = path.parent
        count = count - 1

    carb.log_error(f"Can not find icon path for {__file__}")
    return ""


def set_mode():
    carb.settings.get_settings().set("/app/transform/moveMode", "global")
    carb.settings.get_settings().set("/app/transform/rotateMode", "local")


def selected_prim():
    return omni.usd.get_context().get_selection().get_selected_prim_paths()[0]
