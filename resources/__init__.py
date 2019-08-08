from .dou import get_dou_items
from .dou import get_tracked_fields as _get_dou_tracked
from .lun import get_lun_items
from .lun import get_tracked_fields as _get_lun_tracked
from .olx import get_olx_items, get_new_message, get_message_update
from .olx import get_tracked_fields as _get_olx_tracked

getters = {
    "dou": get_dou_items,
    "lun": get_lun_items,
    "olx": get_olx_items
}

tracked_fields = {
    "dou": _get_dou_tracked(),
    "lun": _get_lun_tracked(),
    "olx": _get_olx_tracked()
}

templates_new = {
    "dou": None,
    "lun": None,
    "olx": get_new_message
}

templates_update = {
    "dou": None,
    "lun": None,
    "olx": get_message_update
}