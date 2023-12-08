import logging
import os
from datetime import datetime, timedelta
from typing import Union

import xarray as xr
from xarray import DataArray, Dataset

from converter.converter_type import ConverterType


def get_input_file_path(file_name: str) -> str:
    """
    Input file name format:
    icon-d2_germany_regular-lat-lon_single-level_2023100212_000_2d_tot_prec.grib2.bz2

    icon-d2 - model name
    germany - region
    regular-lat-lon - grid type
    single-level - level type
    2023100212 - date and time, format: YYYYMMDDHH
    000 - hour shift
    2d_tot_prec - parameter name
    """
    file_meta = file_name.split("_")
    model = file_meta[0].replace("-", "_")
    hour_shift = int(file_meta[5])
    data_datetime = datetime.strptime(file_meta[4], "%Y%m%d%H") + timedelta(hours=hour_shift)
    data_datetime_str = data_datetime.strftime("%d.%m.%Y_%H:%M_%s")

    # Getting the file path
    file_path = model + "/" + data_datetime_str

    return file_path


class Converter:
    input_dir: str = None
    output_dir: str = None
    destinationType: ConverterType = None

    def __init__(self, input_dir: str, output_dir: str, destinationType: ConverterType):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.destinationType = destinationType

    async def convert(self):
        files = sorted(os.listdir(self.input_dir))

        # We should keep previous precipitation values for decreasing
        # from the current values, because grib2 format accumulate
        # data from previous hours
        previous_precipitation: Union[DataArray, Dataset, None] = None

        for file in files:
            logging.info("Converting file: " + file)
            ds = xr.open_dataset(self.input_dir + "/" + file, engine="cfgrib", backend_kwargs={
                "indexpath": "",
            })

            precipitation = ds['tp'] if 'tp' in ds.variables else None

            if precipitation is None:
                logging.info("Skipping no data file: " + file)
                previous_precipitation = None
                continue

            try:
                converted_data = self.destinationType.convert(previous_precipitation, precipitation)
            except Exception as e:
                logging.error("Error while converting file: " + file)
                logging.error(e)
                continue

            previous_precipitation = precipitation

            file_path = get_input_file_path(file)

            # Creating directories
            if not os.path.exists(self.output_dir + "/" + file_path):
                os.makedirs(self.output_dir + "/" + file_path)

            file_name = "PRATE." + self.destinationType.get_extension()
            logging.info("Saving file: " + file_name)
            with open(self.output_dir + "/" + file_path + "/" + file_name, "wb") as f:
                f.write(converted_data)

