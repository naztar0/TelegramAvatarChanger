import logging
import os
import random
from io import BytesIO
from pathlib import Path

ASSETS_PATH = Path('assets/snoo_v1')


def rand_file(path: Path) -> str:
    return path / random.choice([name for name in os.listdir(path)])


async def get_file() -> BytesIO:
    file = rand_file(ASSETS_PATH)
    logging.info(f'Fetching {file}')
    with open(file, 'rb') as f:
        buffer = BytesIO(f.read())
    return buffer


__all__ = ['get_file']
