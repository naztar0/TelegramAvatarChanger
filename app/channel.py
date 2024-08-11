import logging
import random
from io import BytesIO

from telethon import TelegramClient, types
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.types import PeerChannel, MessageEntityTextUrl, KeyboardButtonUrl

from app import CONFIG


async def fetch(client: TelegramClient) -> BytesIO | None:
    config = CONFIG.get()
    channel_peer = PeerChannel(config['channel']['id'])
    total_messages = (await client.get_messages(channel_peer, 0)).total
    offset = random.randint(config['channel']['messages_offset'], total_messages)
    photo: types.Message = (await client.get_messages(channel_peer, 1, offset_id=offset, filter=types.InputMessagesFilterPhotos))[0]

    logging.info(f'Fetched message {photo.id} from {photo.date}')

    url = None
    about = ''

    if photo.reply_markup:
        for row in photo.reply_markup.rows:
            for button in row.buttons:
                if isinstance(button, KeyboardButtonUrl) and button.url:
                    url = button.url
                    break
            if url:
                break
    if not url and photo.entities:
        if entity := next(filter(lambda x: isinstance(x, MessageEntityTextUrl), photo.entities), None):
            url = entity.url

    logging.info(f'URL: {url}')

    if photo.message:
        trim = 24 if url else 68
        about = photo.message[:trim]
        if len(photo.message) > trim:
            about += '… '
    if about and url:
        about += ': ' + url
    elif url:
        about = '🔗 ' + url

    logging.info(f'About: {about}')

    try:
        bfile = BytesIO()
        await client.download_media(photo, bfile)
        bfile.seek(0)
    except ValueError:
        logging.error('Failed to download media')
        return

    await client(UpdateProfileRequest(
        first_name=config['profile']['first_name'],
        last_name=config['profile']['last_name'],
        about=about[:70]
    ))

    return bfile


__all__ = ['fetch']
