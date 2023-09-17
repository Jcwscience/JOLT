import random
import time
from ble_data_transfer import BLEServer
from pack_data import pack_data


pico_server = BLEServer(name="Pi-Pico")

service1 = pico_server.addService(description="DataTransfer", uuid="2e1973f2-558a-11ee-8c99-0242ac120002")

characteristic1 = service1.addCharacteristic(description="Random", uuid="2e197adc-558a-11ee-8c99-0242ac120002", flags=["read", "notify"])

while True:
    random_number = random.randint(0, 100)
    packed_data = pack_data(random_number)
    characteristic1.update(packed_data)
    time.sleep(1)
