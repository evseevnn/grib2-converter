from environs import Env

env = Env()
env.read_env()  # Read .env file


class Config:
    GRIB2_DATA_SOURCE_URL = env.str("GRIB2_DATA_SOURCE_URL")
    MAX_CONCURRENT_DOWNLOADS = env.int("MAX_CONCURRENT_DOWNLOADS", 5)
    DATA_DIR = env.str("DATA_DIR", "data")
    OUTPUT_DIR = env.str("OUTPUT_DIR", "output")
