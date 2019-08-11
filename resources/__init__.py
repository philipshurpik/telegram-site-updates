from .dou import get_dou_items, get_new_message as _get_dou_msg
from .dou import get_tracked_fields as _get_dou_tracked, get_example_link as _get_dou_example
from .lun import get_lun_items, get_new_message as _get_lun_msg, get_message_update as _get_lun_upd
from .lun import get_tracked_fields as _get_lun_tracked, get_example_link as _get_lun_example
from .olx import get_olx_items, get_new_message as _get_olx_msg, get_message_update as _get_olx_upd
from .olx import get_tracked_fields as _get_olx_tracked, get_example_link as _get_olx_example

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
    "lun": _get_lun_upd,
    "olx": _get_olx_upd
}

examples = {
    "dou": _get_dou_example,
    "lun": _get_lun_example,
    "olx": _get_olx_example
}
