import logging
import asyncio
from datetime import datetime

from telethon import TelegramClient, errors, events
from telethon.tl.functions.photos import UploadProfilePhotoRequest
from telethon.tl.functions.account import UpdateProfileRequest

from app import CONFIG


ACTIVE = True
client = TelegramClient('name', CONFIG.get()['api_id'], CONFIG.get()['api_hash'])
client.start(lambda: CONFIG.get()['phone_number'], lambda: CONFIG.get()['2fa_password'])


async def main():
    config = CONFIG.get()
    if config['mode'] == 'snoo_v1':
        from app import snoo_v1
        get_image = snoo_v1.get_file
    elif config['mode'] == 'snoo_v2':
        from app import snoo_v2
        get_image = snoo_v2.generate
    elif config['mode'] == 'txdne':
        from app import txdne
        get_image = txdne.generate
    elif config['mode'] == 'channel':
        from app import channel
        get_image = lambda: channel.fetch(client)
    else:
        raise ValueError('Invalid mode. Must be "snoo_v1", "snoo_v2", "txdne" or "channel"')
    sfw_mode: bool = False
    await client.send_message('me', 'Telegram Avatar Changer started')
    await client.get_dialogs()
    while True:
        if not ACTIVE:
            await asyncio.sleep(1)
            continue
        if (
                config['sfw_mode']['enabled'] and
                config['sfw_mode']['hour_start'] <= datetime.now().hour <= config['sfw_mode']['hour_end'] and
                datetime.now().weekday() in config['sfw_mode']['weekdays']
        ):
            if not sfw_mode:
                logging.info('Switching to SFW mode')
                sfw_mode = True
                await client(UpdateProfileRequest(
                    first_name=config['profile']['first_name'],
                    last_name=config['profile']['last_name'],
                    about=config['profile']['about']
                ))
        elif sfw_mode:
            logging.info('Switching to NSFW mode')
            sfw_mode = False

        bfile = await get_image()
        if bfile is None:
            logging.warning('Failed to fetch image')
            await asyncio.sleep(10)
            continue

        pic = await client.upload_file(bfile, file_name='image.jpg')

        try:
            await client(UploadProfilePhotoRequest(file=pic))
        except errors.rpcerrorlist.PhotoCropSizeSmallError:
            logging.error('Image is too small')
            await asyncio.sleep(10)
            continue

        await asyncio.sleep(config['sleep_time'])


@client.on(events.NewMessage('me', func=lambda e: e.message.message))
async def handler(event: events.NewMessage.Event):
    global ACTIVE
    if event.message.message.lower() == 'stop':
        ACTIVE = False
        await event.reply('Stopped avatar changing')
    elif event.message.message.lower() == 'start':
        ACTIVE = True
        await event.reply('Started avatar changing')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
