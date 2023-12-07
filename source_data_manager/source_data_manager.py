import asyncio
import logging
import os
import re

import aiohttp
import bz2


class SourceDataManager:
    base_url = None
    source_dir = None
    download_dir = None
    max_concurrent_downloads = None

    REGEXP_GET_LINKS = r'<a href="(.*\.grib2\.bz2)">.*</a>'

    def __init__(self, base_url: str, base_data_dir: str, max_concurrent_downloads: int = 5):
        self.base_url = base_url
        self.source_dir = base_data_dir + '/source'
        self.download_dir = base_data_dir + '/download'
        self.max_concurrent_downloads = max_concurrent_downloads

    async def load_source_data_files(self):
        logging.info('Downloading source data files')
        semaphore = asyncio.Semaphore(self.max_concurrent_downloads)
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url) as response:
                # Getting links from the response
                files = re.findall(self.REGEXP_GET_LINKS, await response.text())

                # Create directories
                if not os.path.exists(self.source_dir):
                    os.makedirs(self.source_dir)
                if not os.path.exists(self.download_dir):
                    os.makedirs(self.download_dir)

                tasks = []
                for filename in files:
                    if not os.path.exists(self.download_dir + '/' + filename):
                        task = asyncio.create_task(self.__download_file(session, filename, semaphore))
                        tasks.append(task)
                await asyncio.gather(*tasks)

                # Decompressing files asynchronously
                logging.info('Decompressing files')
                tasks = []
                for filename in files:
                    if not os.path.exists(self.source_dir + '/' + filename[:-4]):
                        task = asyncio.create_task(self.__decompress_file(filename))
                        tasks.append(task)

                await asyncio.gather(*tasks)

    async def __download_file(self, session: aiohttp.ClientSession, url: str, semaphore):
        """
        Download file from the data source
        :param semaphore:
        :param session: aiohttp session
        :param url: file url
        :return: None
        """
        async with semaphore:
            logging.info('Downloading file: ' + url)
            async with session.get(self.base_url + url) as response:
                with open(self.download_dir + '/' + url, 'wb') as f:
                    while True:
                        chunk = await response.content.read(1024)
                        if not chunk:
                            break
                        f.write(chunk)

                logging.info('File downloaded: ' + url)

    async def __decompress_file(self, filename):
        """
        Decompress file
        :param filename: file name
        :return: None
        """
        logging.info('Decompressing file: ' + filename)
        with open(self.download_dir + '/' + filename, 'rb') as source, \
                open(self.source_dir + '/' + filename[:-4], 'wb') as destination:
            destination.write(bz2.decompress(source.read()))
        logging.info('File decompressed: ' + filename)
