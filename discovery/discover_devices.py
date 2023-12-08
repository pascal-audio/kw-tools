# SPDX-License-Identifier: MIT

from zeroconf import ServiceBrowser, ServiceListener, Zeroconf

class MyListener(ServiceListener):
    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        print(f"Service {name} updated")

    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        print(f"Service {name} removed")

    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        info = zc.get_service_info(type_, name)
        
        print(f"Device added: {info.name}")

        p = info.properties
        api_version = p.get(b'api_version', b'').decode()
        serial = p.get(b'serial', b'').decode()
        vendor = p.get(b'vendor', b'').decode()
        model = p.get(b'model', b'').decode()
        device_class = p.get(b'device_class', b'').decode()
        firmware_version = p.get(b'firmware_version', b'').decode()
        
        print(f"    Vendor:  {vendor}")
        print(f"    Model:   {model}")
        print(f"    Serial:  {serial}")
        print(f"    Class:   {device_class}")
        print(f"    API Ver: {api_version}")
        print(f"    FW Ver:  {firmware_version}")


zeroconf = Zeroconf()
listener = MyListener()
browser = ServiceBrowser(zeroconf, "_pasconnect._tcp.local.", listener)
try:
    input("Press enter to exit...\n\n")
finally:
    zeroconf.close()