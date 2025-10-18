import pyudev
from typing import Optional

def retrieve_usb_disk_device_node(vendor_id: int, prod_id: int) -> Optional[str]:
    """
    Get USB disk device node (e.g. /dev/sda) for the device with the
    corresponding vendor and product ID.
    """
    ctx = pyudev.Context()
    target_vendor_str = "{:04X}".format(vendor_id)
    target_prod_str = "{:04X}".format(prod_id)
    for device in ctx.list_devices(DEVTYPE='disk', subsystem='block'):
        props = device.properties
        dev_vendor_id = props['ID_VENDOR_ID'] if 'ID_VENDOR_ID' in props else ''
        dev_prod_id = props['ID_USB_MODEL_ID'] if 'ID_USB_MODEL_ID' in props else ''
        if dev_vendor_id == target_vendor_str and target_prod_str:
          return props['DEVNAME']
    return None
