import asyncio
import logging

import aiorun as aiorun

from config import Config
from source_data_manager.source_data_manager import SourceDataManager

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


async def async_main():
    logging.info('Initializing')
    source_data_manager = SourceDataManager(
        base_url=Config.GREP2_DATA_SOURCE_URL,
        base_data_dir=Config.DATA_DIR,
        max_concurrent_downloads=Config.MAX_CONCURRENT_DOWNLOADS
    )

    logging.info('Loading source data files')
    await source_data_manager.load_source_data_files()

    logging.info('Done')
    asyncio.get_event_loop().stop()

if __name__ == '__main__':
    aiorun.run(async_main(), stop_on_unhandled_errors=True)
