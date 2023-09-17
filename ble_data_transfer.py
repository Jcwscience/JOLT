import bluetooth
from micropython import const
from ble_advertising import advertising_payload

# BLE related constants
_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)

_FLAG_READ = const(0x0002)
_FLAG_WRITE = const(0x0008)
_FLAG_NOTIFY = const(0x0010)

class BLEServer:
    def __init__(self, name="Pi-Pico"):
        self._ble = bluetooth.BLE()
        self._ble.active(True)
        self._connections = set()
        self._services = []

        self._payload = advertising_payload(name=name)
        self._advertise()

    def addService(self, description, uuid):
        new_service = BLEService(self._ble, description, uuid, self._connections)
        self._services.append(new_service)
        return new_service

    def _advertise(self, interval_us=500000):
        self._ble.gap_advertise(interval_us, adv_data=self._payload)

class BLEService:
    def __init__(self, ble, description, uuid, connections):
        self._ble = ble
        self._description = description
        self._uuid = bluetooth.UUID(uuid)
        self._connections = connections
        self._characteristics = []

    def addCharacteristic(self, description, uuid, flags):
        new_char = BLECharacteristic(self._ble, description, uuid, flags, self._connections, self._uuid)
        self._characteristics.append(new_char)
        return new_char

class BLECharacteristic:
    def __init__(self, ble, description, uuid, flags, connections, service_uuid):
        self._ble = ble
        self._description = description
        self._uuid = bluetooth.UUID(uuid)
        self._service_uuid = service_uuid
        self._flags = 0

        if "read" in flags:
            self._flags |= _FLAG_READ
        if "write" in flags:
            self._flags |= _FLAG_WRITE
        if "notify" in flags:
            self._flags |= _FLAG_NOTIFY

        characteristic_tuple = (self._uuid, self._flags)
        service_tuple = (self._service_uuid, (characteristic_tuple,))
        ((self._handle,),) = self._ble.gatts_register_services((service_tuple,))


        self._connections = connections

    def update(self, data):
        self._ble.gatts_write(self._handle, data)
        for conn_handle in self._connections:
            self._ble.gatts_notify(conn_handle, self._handle)

    def read(self):
        return self._ble.gatts_read(self._handle)

# Create a convenient alias for classes to make them feel like functions
server = BLEServer
service = BLEService
characteristic = BLECharacteristic
