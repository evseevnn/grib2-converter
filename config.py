from environs import Env

env = Env()
env.read_env()  # Read .env file


class Config:
    GREP2_DATA_SOURCE_URL = env.str("GREP2_DATA_SOURCE_URL")
