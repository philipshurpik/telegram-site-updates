from .dou import get_dou_items, get_new_message as _get_dou_msg
from .dou import get_tracked_fields as _get_dou_tracked
from .lun import get_lun_items, get_new_message as _get_lun_msg
from .lun import get_tracked_fields as _get_lun_tracked
from .olx import get_olx_items, get_new_message as _get_olx_msg, get_message_update
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
    "dou": _get_dou_msg,
    "lun": _get_lun_msg,
    "olx": _get_olx_msg
}

templates_update = {
    "dou": None,
    "lun": None,
    "olx": get_message_update
}