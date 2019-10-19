import myo
from myo import *
from PyQt5.QtCore import QThread, pyqtSignal, QTimer


class Listener(DeviceListener):
    def __init__(self, m):
        super().__init__()
        self.manager = m
        self.data = {}

    def on_connected(self, event):
        self.manager.connecting = False
        self.manager.connected = True

        event.device.request_battery_level()
        event.device.request_rssi()

        event.device.stream_emg(True)
        event.device.vibrate(myo.VibrationType.short)

        self.manager.signals.emit({"type": event.type,
                                   "data": {"name": event.device_name,
                                            "mac_address": event.mac_address}})

    def on_disconnected(self, event):
        self.manager.signals.emit({"type": event.type,
                                   "data": {"timeout": "",
                                            "unOpenMyo": ""}})
        self.manager.connected = False

    def on_emg(self, event):
        self.manager.signals.emit({"type": event.type,
                                   "data": {"emg": event.emg}})

    def on_orientation(self, event):
        self.manager.signals.emit({"type": event.type,
                                   "data": {"gyroscope": event.gyroscope,
                                            "acceleration": event.acceleration,
                                            "orientation": event.orientation}})

    def on_battery_level(self, event):
        self.manager.signals.emit({"type": event.type,
                                   "data": {"battery": event.battery_level}})

    def on_rssi(self, event):
        self.manager.signals.emit({"type": event.type,
                                   "data": {"rssi": event.rssi}})


class MyoManager(QThread):
    signals = pyqtSignal(dict)
    send = None
    connecting = False
    connected = False

    def __init__(self, sender):
        super().__init__()
        self.send = sender
        self.signals.connect(sender.callback)
        myo.init(sdk_path=r'C:\myo-sdk-win-0.9.0')

    def timed_out(self):
        if (not self.connected) and self.connecting:
            self.signals.emit({"type": EventType.disconnected,
                               "data": {"timeout": "timeout",
                                        "unOpenMyo": ""}})
            self.disconnect()

    def connect(self):
        if not self.connected and not self.connecting:
            self.connecting = True
            self.stop = False
            QTimer.singleShot(5000, self.timed_out)
            self.start()

    def run(self):
        try:
            self.listener = Listener(self)
            hub = myo.Hub("com.twins.dataset")

            while hub.run(self.listener.on_event, 500):
                if self.stop:
                    self.stop = False
                    break
        except:
            self.signals.emit({"type": EventType.disconnected,
                               "data": {"timeout": "",
                                        "unOpenMyo": "unOpenMyo"}})
            self.connecting = False

    def disconnect(self):
        if self.connected:
            self.signals.emit({"type": EventType.disconnected,
                               "data": {"timeout": "",
                                        "unOpenMyo": ""}})
        self.connecting = False
        self.connected = False
        self.stop = True
