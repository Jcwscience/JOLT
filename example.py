import bluetooth
import random
import time
from ble_data_transfer import BLEManager
from pack_data import pack_data



_FLAG_READ = const(0x0002)
_FLAG_NOTIFY = const(0x0010)
_FLAG_INDICATE = const(0x0020)

_SERVICE_UUID = bluetooth.UUID("c04cd54e-6c04-4fa2-8afb-93ac92e4a8fe")

_CHARACTERISTIC = (bluetooth.UUID("1dc2422c-b770-4125-acc7-a5be80b6565e"),
_FLAG_READ | _FLAG_NOTIFY | _FLAG_INDICATE,)

_SERVICE = (_SERVICE_UUID,(_CHARACTERISTIC,),)


manager = BLEManager(ble=bluetooth.BLE(), name="Pi-Pico", service=_SERVICE)

while True:
    packed_int = pack_data(random.randint(0,100))
    packed_string = pack_data("Test String")
    manager.update_data(packed_int, notify=True, indicate=False)
    manager.update_data(packed_string, notify=True, indicate=False)
    time.sleep_ms(1000)
