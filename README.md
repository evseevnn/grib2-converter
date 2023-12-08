# GRIP2 to WFG4 Converter

This is a simple converter from GRIP2 to WFG4.

## Configuration

Default values:
```
GRIB2_DATA_SOURCE_URL=https://opendata.dwd.de/weather/nwp/icon-d2/grib/12/tot_prec/
MAX_CONCURRENT_DOWNLOADS=5
DATA_DIR=data
OUTPUT_DIR=output
```

You can change default values by setting environment variables or by creating `.env` file in the root of the project.
Example of `.env` file available in `.env.example`.

## Installation

1. First you need install poetry.
```
pip3 install poetry
```

2. Then you need to install dependencies.
```
poetry install
```

## Usage

For running the converter you need to install python3 and pip3.
```
python3 main.py
```

## Notes

1. The converter is not tested on Windows.

2. You can use `wfg4reader.php` for as example of reading WFG4 files on PHP.

## TODO

- [ ] Add tests


