
import logging

from client import (
    DataProvider
)
from extractor import (
    DataExtractor,
)


def get_data_extractor() -> DataExtractor:
    logger = logging.Logger
    client = DataProvider(logger)
    extractor = DataExtractor(client, logger)

    return extractor
