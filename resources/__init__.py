from .dou import get_dou_items
from .lun import get_lun_items
from .olx import get_olx_items

getters = {
    "dou": get_dou_items,
    "lun": get_lun_items,
    "olx": get_olx_items
}
