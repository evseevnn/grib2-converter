import struct
from dataclasses import dataclass

import numpy as np
from xarray import Dataset, DataArray

from converter.converter_type import ConverterType

PRECISION_SCALE: int = 1000000  # we need to multiply the values to get integer values
SPECIAL_MARKER: float = -100500.00  # special marker for "no value" or header marker


@dataclass
class WGF4Header:
    """
    Header of the WGF4 file.
    """
    lat_min: int
    lat_max: int
    long_min: int
    long_max: int
    lat_step: int
    long_step: int
    multiplier: int

    @classmethod
    def from_data(cls, lats: DataArray, longs: DataArray) -> "WGF4Header":
        lat_min = int(lats.min() * PRECISION_SCALE)
        lat_max = int(lats.max() * PRECISION_SCALE)
        long_min = int(longs.min() * PRECISION_SCALE)
        long_max = int(longs.max() * PRECISION_SCALE)

        lat_step = (lat_max - lat_min) // lats.shape[0]
        long_step = (long_max - long_min) // longs.shape[0]

        return cls(
            lat_min, lat_max, long_min, long_max, lat_step, long_step, PRECISION_SCALE
        )

    def to_bytes(self) -> bytes:
        """
        Converts header to bytes.
        This also will add special marker to the end of the header.
        :return:
        """
        return struct.pack(
            "7i",
            self.lat_min, self.lat_max, self.long_min, self.long_max,
            self.lat_step, self.long_step, self.multiplier
        )


class WGF4(ConverterType):
    """
    Class for WGF4 type converter.
    """

    def convert(self, prev_values: DataArray, values: DataArray) -> bytes:
        """
        Converts GRIB2 dataset to WFG4 format and return in bytes
        """
        header = WGF4Header.from_data(values.latitude, values.longitude).to_bytes()
        separator = struct.pack("f", SPECIAL_MARKER)

        flatten_data: np.array = values.to_numpy().flatten()

        # We should decrease current values from previous values
        if prev_values is not None:
            prev_flatten_data = prev_values.to_numpy().flatten()

            # ICON-2D model can have different shapes of the data for latest hour of prediction (48 hours forecast)
            if flatten_data.shape < prev_flatten_data.shape:
                # case with 48 hours forecast
                prev_flatten_data = prev_flatten_data[:flatten_data.shape[0]]
                flatten_data = flatten_data - prev_flatten_data
            elif flatten_data.shape == prev_flatten_data.shape:
                flatten_data = flatten_data - prev_flatten_data

        # All values should be multiplied by the precision scale
        flatten_data = flatten_data * PRECISION_SCALE

        # replace nan values with special marker
        flatten_data = np.nan_to_num(flatten_data, nan=SPECIAL_MARKER)

        # getting bytes from the array
        data_bytes = flatten_data.astype(np.int32).tobytes()

        return header + separator + data_bytes
