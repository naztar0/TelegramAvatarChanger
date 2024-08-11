import logging
import random
from io import BytesIO
import requests

# Get source from https://thisxdoesnotexist.com
#
# https://thispersondoesnotexist.com
# https://www.thiswaifudoesnotexist.net/example-{num}.jpg // 0..100000
# https://thisfursonadoesnotexist.com/v2/jpgs-2x/seed{num}.jpg // 0..99999 .zfill(5)
# https://thisponydoesnotexist.net/v1/w2x-redo/jpgs/seed{num}.jpg // 0..99999 .zfill(5)

SOURCE = 'https://www.thiswaifudoesnotexist.net/example-{num}.jpg'


async def generate():
    num = random.randint(0, 100000)
    try:
        req = requests.get(SOURCE.format(num=num))
    except Exception as e:
        logging.error(e)
        return
    if req.status_code != 200:
        logging.error(f'Failed to fetch image: {req.status_code}')
        return
    return BytesIO(req.content)


__all__ = ['generate']
