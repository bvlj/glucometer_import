# SPDX-FileCopyrightText: © 2020 The glucometerutils Authors
# SPDX-License-Identifier: MIT

import abc
import dataclasses
import datetime
import importlib
import inspect
from typing import Generator, Optional, Text, Type

from glucometerutils import common


class GlucometerDevice(abc.ABC):
    def __init__(self, device_path: Optional[Text]) -> None:
        pass

    def connect(self) -> None:
        pass

    def disconnect(self) -> None:
        pass

    @abc.abstractmethod
    def get_meter_info(self) -> common.MeterInfo:
        """
        Return the device information in structured form.
        """
        pass

    @abc.abstractmethod
    def get_serial_number(self) -> str:
        pass

    @abc.abstractmethod
    def get_glucose_unit(self) -> common.Unit:
        """
        Returns the glucose unit of the device.
        """
        pass

    @abc.abstractmethod
    def get_readings(self) -> Generator[common.AnyReading, None, None]:
        pass


@dataclasses.dataclass
class Driver:
    device: Type[GlucometerDevice]
    help: str


def load_driver(driver_name: str) -> Driver:
    driver_module = importlib.import_module(f"glucometerutils.drivers.{driver_name}")
    help_string = inspect.getdoc(driver_module)
    assert help_string is not None

    return Driver(getattr(driver_module, "Device"), help_string)
