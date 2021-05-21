from typing import Tuple, Optional

import serial
import pynmea2


class GPSNotConnectedError(Exception):
    pass


def get_current_lat_lon(attempts: Optional[int] = 100) -> Tuple[float, float]:
    ser = serial.Serial('/dev/serial0', 9600, timeout=0.2)
    current_attempt = 0
    while True:
        current_attempt += 1
        try:
            recv = ser.readline().decode()
            if recv.startswith('$'):
                record = pynmea2.parse(recv)
                if recv.startswith('$GPRMC') or recv.startswith('$GNRMC'):
                    if record.status == 'V':
                        raise GPSNotConnectedError
                    else:
                        return record.latitude, record.longitude
        except pynmea2.nmea.ParseError:
            raise GPSNotConnectedError
        if current_attempt > attempts:
            raise GPSNotConnectedError
